import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from starlette.requests import Request

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.banking.accounting import deposit, withdraw
from src.core.core import get_jwt_key
from src.banking.exceptions import no_acct, insufficient_funds

sys.path.insert(0, str(Path(__file__).parent.parent))

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher

from src.banking import verify_pin
from src.crypto.exceptions import incorrect_pin


class Login(BaseModel):
    pin: str


app = FastAPI()
ph = PasswordHasher()

def generate_token(account_number, pin):
    try:
        verify_pin(account_number, pin)
    except incorrect_pin:
        raise incorrect_pin

    key = get_jwt_key()
    ph_tz = timezone(timedelta(hours=8))

    return jwt.encode(
        {
            "account_number": account_number,
            "iat": datetime.now(ph_tz)
        },
        key, algorithm="HS256"
    )

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ("/login/", "/docs", "/openapi.json", "/redoc")

        if request.url.path.endswith(public_paths):
            return await call_next(request)
        else:
            jwt_key = get_jwt_key()

            jwt_token = request.headers.get("Authorization")
            if not jwt_token or not jwt_token.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"message": "Missing JWT Token"})
            else:
                jwt_token = jwt_token.split(" ")[1]
                payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])

                acct_number = payload["account_number"]
                request.state.account_number = acct_number
                if bool(payload):
                    return await call_next(request)
                else:
                    return JSONResponse(status_code=403, content={"message": "Incorrect JWT Token"})

@app.post("/{account_number}/login/")
def login(pin: Login, account_number: str):
    try:
        token = generate_token(account_number, pin.pin)
    except incorrect_pin:
        raise HTTPException(status_code=403, detail="Incorrect PIN")
    except no_acct:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"token": token}

@app.post("/deposit")
def Deposit(amount: int, request: Request, pin: Login):
    pin = str(pin.pin)
    account_number = request.state.account_number
    try:
        new_bal = deposit(amount, account_number, pin)
    except incorrect_pin:
        raise HTTPException(status_code=403, detail="Incorrect PIN")
    except no_acct:
        raise HTTPException(status_code=404, detail="Account not found")

    return {
        "status": "ok",
        "new_balance": new_bal
    }

@app.post("/withdraw")
def Withdraw(amount: int, request: Request, pin: Login):
    pin = str(pin.pin)
    account_number = request.state.account_number
    try:
        new_bal = withdraw(amount, account_number, pin)
    except incorrect_pin:
        raise HTTPException(status_code=403, detail="Incorrect PIN")
    except insufficient_funds:
        raise HTTPException(status_code=409, detail="Insufficient funds")
    except no_acct:
        raise HTTPException(status_code=404, detail="Account not found")

    return {
        "status": "ok",
        "new_balance": new_bal
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

app.add_middleware(AuthMiddleware)