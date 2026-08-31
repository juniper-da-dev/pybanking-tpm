import keyring
from dotenv import load_dotenv

load_dotenv()

def test_Master_Key():
    assert keyring.get_password("Banking", "master_key")
