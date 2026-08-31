from .banking import verify_pin
from ..crypto.exceptions import incorrect_pin
from .database import get_data, store_data
from .exceptions import insufficient_funds, invalid_amount


def withdraw(amount, account, pin):
    try:
        verify_pin(account, pin)
    except incorrect_pin:
        raise incorrect_pin

    current_balance = get_data(account, "balance", pin)
    if not isinstance(amount, (float, int)):
        raise TypeError("amount must be a float")

    if float(amount) < 0:
        raise invalid_amount
    elif float(current_balance) < float(amount):
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

    if not isinstance(amount, (float, int)):
        raise TypeError("amount must be a float")
    elif float(amount) < 0:
        raise invalid_amount

    current_balance = get_data(account, "balance", pin)
    new_balance = float(current_balance) + float(amount)
    store_data(account, "balance", new_balance, pin)
    return new_balance