from src.banking import get_data, store_data


def test_storing():
    store_data("0000-0000-0000", "name", "tung tung talion", "0601214")
    assert get_data("0000-0000-0000", "name", "0601214") == "tung tung talion"

def test_retrival():
    store_data("0000-0000-0000", "balance", "0", "0601214")
    assert get_data("0000-0000-0000", "balance", "0601214") == "0"