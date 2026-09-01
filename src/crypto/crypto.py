import base64
import hashlib
import os
from typing import Optional

from argon2 import PasswordHasher
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .exceptions import incorrect_pin, missing_pin
from ..core import get_master_key

ph = PasswordHasher()

def encrypt(data, pin, nopin=False):
    if not nopin:
        master_key = get_master_key()
        hpin = hashlib.sha256(pin.encode()).hexdigest()
        ckey = master_key + hpin.encode()
        dkey = hashlib.sha256(ckey).digest()

        nonce = os.urandom(12)

        cipher = AESGCM(dkey)
        ciphertext = cipher.encrypt(nonce, str(data).encode(), None)

        return base64.b64encode(nonce + ciphertext).decode()
    else:
        master_key = get_master_key()

        nonce = os.urandom(12)

        cipher = AESGCM(master_key)
        ciphertext = cipher.encrypt(nonce, str(data).encode(), None)

        return "NOPIN-" + base64.b64encode(nonce + ciphertext).decode()


def decrypt(data, pin: Optional[str] = None):
    if data[:6] == "NOPIN-":
        master_key = get_master_key()

        data = data[6:]
        data = base64.b64decode(data)
        nonce = data[:12]
        encrypted_data = data[12:]

        try:
            cipher = AESGCM(master_key)
            unencrypted_text = cipher.decrypt(nonce, encrypted_data, None).decode()
        except InvalidTag:
            raise incorrect_pin

        return str(unencrypted_text)
    else:
        try:
            master_key = get_master_key()
            hpin = hashlib.sha256(pin.encode()).hexdigest()
            ckey = master_key + hpin.encode()
            dkey = hashlib.sha256(ckey).digest()
            data = base64.b64decode(data)

            nonce = data[:12]
            encrypted_data = data[12:]

            cipher = AESGCM(dkey)
            decrypted_text = cipher.decrypt(nonce, encrypted_data, None).decode()

            return str(decrypted_text)
        except InvalidTag:
            raise incorrect_pin



