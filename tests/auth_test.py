import pytest
import keyring
from ast import literal_eval
from cryptography.fernet import Fernet
from unittest.mock import patch, MagicMock
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

    # Decrypt the password
    decrypted_password = decrypt(master_password, encrypted_password, salt)

    # Ensure the decrypted password matches the original password
    # test
    assert decrypted_password == password

# masterkey storage test
@patch('keyring.set_password')
def test_store_masterkey(mock_creds):
    store_masterkey("fakekey123")
    mock_creds.assert_called_once_with("pwtool", "admin", "fakekey123")

# encrypt test
def test_encrypt():
    master_pass = "StrongPassword1!"
    password = "Secret123"
    salt=b"1234567890123456"

    encrypted = encrypt(master_pass, password, salt)

    assert isinstance(encrypted, bytes) # check if in binary
    assert len(encrypted) > 0

# proper decryption test
@patch("pwtool.auth.derive_fernet_key_argon2", return_value=b"f" * 32)
@patch("pwtool.auth.Fernet")
def test_decrypt(mock_fernet_class, mock_derive):
    mock_fernet = MagicMock()
    mock_fernet.decrypt.return_value = b"password"
    mock_fernet_class.return_value = mock_fernet

    encrypted = b'fake_encrypted'
    result = decrypt("masterpw", encrypted, b'salt')

    mock_derive.assert_called_once_with("masterpw", b'salt')
    mock_fernet.decrypt.assert_called_once_with(b'fake_encrypted')
    assert result == "password"