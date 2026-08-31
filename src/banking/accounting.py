from .banking import verify_pin
from crypto.exceptions import incorrect_pin
from .database import get_data, store_data
from .exceptions import insufficient_funds

def withdraw(amount, account, pin):
    try:
        verify_pin(account, pin)
    except incorrect_pin:
        raise incorrect_pin

    current_balance = get_data(account, "balance", pin)
    if float(current_balance) < float(amount):
        raise insufficient_funds
    else:
        new_balance = float(current_balance) - float(amount)
        store_data(account, "balance", new_balance, pin)
        return new_balance

def deposit(amount, account, pin):
    try:
        verify_pin(account, pin)
    except incorrect_pin:
        raise incorrect_pin

    current_balance = get_data(account, "balance", pin)
    new_balance = float(current_balance) + float(amount)
    store_data(account, "balance", new_balance, pin)
    return new_balance