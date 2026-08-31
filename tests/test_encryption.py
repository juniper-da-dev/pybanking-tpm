from crypto import decrypt, encrypt


def test_Encryption():
    etext = encrypt("i fuckin love tomboys", "1212")
    print(etext)

    assert etext is not None
    assert isinstance(etext, str)

def test_Decryption():
    etext = encrypt("i fuckin love femboys", "1212")
    dtext = decrypt(etext, "1212")

    assert dtext is not None and dtext == "i fuckin love femboys"
    assert isinstance(dtext, str)

