import base64
import os
import secrets

import keyring

# Helper Functions - Core

def MasterKey_INIT():
    master_key = os.urandom(32)
    key = base64.b64encode(master_key).decode()
    keyring.set_password("Banking", "master_key", key)

    return key

def MasterKeyJWT_INIT():
    jwt_key = secrets.token_urlsafe(32)
    keyring.set_password("Banking", "jwt_key", jwt_key)

    return jwt_key


def get_master_key():
    master = keyring.get_password("Banking", "master_key")
    assert master is not None

    master_key_bytes = base64.b64decode(master)

    return master_key_bytes

def get_jwt_key():
    jwt = keyring.get_password("Banking", "jwt_key")
    assert jwt is not None

    return jwt


if keyring.get_password("Banking", "master_key"):
    pass
else:
    MasterKey_INIT()
    print("Master Key initialized")

if keyring.get_password("Banking", "jwt_key"):
    pass
else:
    MasterKeyJWT_INIT()
    print("JWT Key initialized")