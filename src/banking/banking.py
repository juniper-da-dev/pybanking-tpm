from argon2 import PasswordHasher
from .database import store_data, get_data
from argon2.exceptions import VerifyMismatchError
from crypto.exceptions import incorrect_pin
import secrets

ph = PasswordHasher()

def open_account(name, pin):
    account = str(secrets.randbelow(9999)).zfill(4) + "-" + str(secrets.randbelow(9999)).zfill(4) + "-" + str(secrets.randbelow(9999)).zfill(4) + "-" + str(secrets.randbelow(9999)).zfill(4)
    hpin = ph.hash(pin)

    store_data(account, "balance", "0", pin)
    store_data(account, "name", name, pin)
    store_data(account, "PIN", hpin, nopin=True)

    return account

def verify_pin(account, pin):
    stored_pin = get_data(account, "PIN")
    try:
        ph.verify(str(stored_pin), str(pin))
    except VerifyMismatchError:
        raise incorrect_pin

def change_info(account, info, data, pin):
    try:
        verify_pin(account, pin)
    except incorrect_pin:
        raise incorrect_pin

    if info == "name":
        store_data(account, "name", data, pin)
    elif info == "pin":
        existing_name = get_data(account, "name", pin)
        existing_balance = get_data(account, "balance", pin)
        pin = data

        store_data(account, "PIN", str(ph.hash(data)), nopin=True)
        store_data(account, "balance", existing_balance, pin)
        store_data(account, "name", existing_name, pin)
