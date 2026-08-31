import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import jwt
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher

from src.banking.banking import verify_pin
from src.core import get_master_key
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

    key = get_master_key()

    return jwt.encode(
        {
            "account_number": account_number,
            "iat": datetime.datetime.now()
        },
        key, algorithm="HS256"
    )

@app.post("/{account_number}/login/")
def login(pin: Login, account_number: str):
    try:
        token = generate_token(account_number, pin.pin)
    except incorrect_pin:
        return HTTPException(status_code=403, detail="Incorrect PIN")
    return {"token": token}
