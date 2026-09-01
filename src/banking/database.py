import shelve
from pathlib import Path
from typing import Optional

from ..crypto import encrypt, decrypt
from ..crypto.exceptions import incorrect_pin, missing_pin

accounts = str(Path(__file__).parent.parent.parent / "accounts")

def store_data(account, name, key, pin: Optional[str] = None, nopin=False):
    with shelve.open(accounts, writeback=True) as db:
        if not nopin:
            key = encrypt(key, pin)
            if account not in db:
                db[account] = {}
            db[account][name] = key
        else:
            key = encrypt(key, pin, nopin=True)
            if account not in db:
                db[account] = {}
            db[account][name] = key


def get_data(account, name, pin: Optional[str] = None):
    from ..banking.exceptions import no_key, no_acct

    if pin:
        with shelve.open(accounts, writeback=True) as db:
            if account not in db:
                raise no_acct
            elif name not in db[account]:
                raise no_key
            try:
                key = decrypt(db[account][name], pin)
            except incorrect_pin:
                raise incorrect_pin

            return key
    else:
        with shelve.open(accounts, writeback=True) as db:
            if account not in db:
                raise no_acct
            elif name not in db[account]:
                raise no_key
            unencrypted_data = db[account][name]
            if unencrypted_data[:6] != "NOPIN-":
                raise missing_pin
            else:
                try:
                    decrypted_data = decrypt(unencrypted_data, pin)
                    return decrypted_data
                except incorrect_pin:
                    raise incorrect_pin

