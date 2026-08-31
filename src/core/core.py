import base64
import os

import keyring

# Helper Functions - Core

def MasterKey_INIT():
    master_key = os.urandom(32)
    key = base64.b64encode(master_key).decode()
    keyring.set_password("Banking", "master_key", key)

    return key


def get_master_key():
    master = keyring.get_password("Banking", "master_key")
    assert master is not None

    master_key_bytes = base64.b64decode(master)

    return master_key_bytes


if keyring.get_password("Banking", "master_key"):
    pass
else:
    MasterKey_INIT()
    print("Master Key initialized")