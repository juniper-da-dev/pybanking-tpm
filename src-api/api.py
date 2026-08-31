import sys
from operator import contains
from pathlib import Path
from starlette.requests import Request

from starlette.middleware.base import BaseHTTPMiddleware

from src.core.core import get_jwt_key
from src.banking.exceptions import no_acct

sys.path.insert(0, str(Path(__file__).parent.parent))

import jwt
import datetime
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
    print(key)

    return jwt.encode(
        {
            "account_number": account_number,
            "iat": datetime.datetime.now()
        },
        key, algorithm="HS256"
    )

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ("/login", "/docs", "/openapi.json")

        if request.url.path.endswith(public_paths):
            return await call_next(request)
        else:
            jwt_key = get_jwt_key()

            jwt_token = request.headers.get("Authorization")
            if not jwt_token or not jwt_token.startswith("Bearer "):
                raise HTTPException(status_code=403, detail="Missing JWT Token")
            else:
                jwt_token = jwt_token.split(" ")[1]
                payload = jwt.decode(jwt_token, jwt_key, algorithms=["HS256"])

                acct_number = payload["account_number"]
                request.state.account_number = acct_number
                if bool(payload):
                    return await call_next(request)
                else:
                    raise HTTPException(status_code=403, detail="Incorrect JWT Token")

@app.post("/{account_number}/login/")
def login(pin: Login, account_number: str):
    try:
        token = generate_token(account_number, pin.pin)
    except incorrect_pin:
        raise HTTPException(status_code=403, detail="Incorrect PIN")
    except no_acct:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"token": token}

app.get("/test")
def test():
    return {
        "message": "test"
    }

app.add_middleware(AuthMiddleware)