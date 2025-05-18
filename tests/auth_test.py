import pytest
import keyring
from ast import literal_eval
from cryptography.fernet import Fernet
from unittest.mock import patch, MagicMock
from pwtool.auth import encrypt, decrypt, store_masterkey, derive_fernet_key_argon2

def test_encrypt_decrypt():
    master_password = "TestMasterPassword"
    password = "TestPassword123"
    salt = b"1234567890123456"  # 16 bytes salt
    key = derive_fernet_key_argon2(password, salt)

    # Encrypt the password
    encrypted_password = encrypt(password, salt, key=key)

    # Ensure the encrypted password is not None or empty
    assert encrypted_password is not None
    assert len(encrypted_password) > 0

    # Decrypt the password
    decrypted_password = decrypt(encrypted_password, salt, key=key)

    # Ensure the decrypted password matches the original password
    # test
    assert decrypted_password == password

# masterkey storage test
@patch('keyring.set_password')
def test_store_masterkey(mock_creds):
    store_masterkey("fakekey123")
    mock_creds.assert_called_once_with("pwtool", "admin", "fakekey123")

def test_deprecated_encrypt_with_pass():
    master_pass = "StrongPassword1!"
    password = "Secret123"
    salt=b"1234567890123456"

    encrypted = encrypt(password, salt, master_password=master_pass)

    assert isinstance(encrypted, bytes) # check if in binary
    assert len(encrypted) > 0

@patch("pwtool.auth.derive_fernet_key_argon2", return_value=b"f" * 32)
@patch("pwtool.auth.Fernet")
def test_deprecated_decrypt_with_pass(mock_fernet_class, mock_derive):
    mock_fernet = MagicMock()
    mock_fernet.decrypt.return_value = b"password"
    mock_fernet_class.return_value = mock_fernet

    encrypted = b'fake_encrypted'
    result = decrypt(encrypted, b'salt', master_password="masterpw")

    mock_derive.assert_called_once_with("masterpw", b'salt')
    mock_fernet.decrypt.assert_called_once_with(b'fake_encrypted')
    assert result == "password"