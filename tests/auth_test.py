import pytest
import keyring
from unittest.mock import patch
import pwtool.storage
from pwtool.auth import encrypt, decrypt, store_masterkey

def test_encrypt_decrypt():
    master_password = "TestMasterPassword"
    password = "TestPassword123"
    salt = b"1234567890123456"  # 16 bytes salt

    # Encrypt the password
    encrypted_password = encrypt(master_password, password, salt)

    # Ensure the encrypted password is not None or empty
    assert encrypted_password is not None
    assert len(encrypted_password) > 0

    # Convert the encrypted password to a string representation
    encrypted_password_str = repr(encrypted_password)

    # Decrypt the password
    decrypted_password = decrypt(master_password, encrypted_password_str, salt)

    # Ensure the decrypted password matches the original password
    # test
    assert decrypted_password == password

@patch('keyring.set_password')
def test_store_masterkey(mock_creds):
    store_masterkey("fakekey123")
    mock_creds.assert_called_once_with("pwtool", "admin", "fakekey123")