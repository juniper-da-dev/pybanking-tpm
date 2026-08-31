from banking.accounting import *
from banking.database import *

def test_withdrawals():
    store_data("0000-0000-0000-0000", "balance", "1000", "1234")
    new_balance = withdraw(1000, "0000-0000-0000-0000", "1234")
    assert new_balance == 0.0

def test_deposits():
    new_balance = deposit(1000, "0000-0000-0000-0000", "1234")
    assert new_balance == 1000.0
    store_data("0000-0000-0000-0000", "balance", "0", "1234")