import pytest
from models import Password, App
from unittest.mock import patch, MagicMock

# Test for Password class
def test_password_initialization():
    password = Password(length=16, service="test_service", username="test_user")
    assert password.length == 16
    assert password.service == "test_service"
    assert password.username == "test_user"
    assert len(password.password) == 16

def test_password_generation():
    password = Password(length=20, service="test_service", username="test_user")
    assert len(password.password) == 20
    assert any(char.isupper() for char in password.password)  # At least one uppercase
    assert any(char.islower() for char in password.password)  # At least one lowercase
    assert any(char.isdigit() for char in password.password)  # At least one digit
    assert any(char in '!@#$%^&*()_+-={}[]|:;\"\'<>,.?/~`' for char in password.password)  # At least one special character

def test_password_save():
    with patch("models.save_pass") as mock_save_pass:
        password = Password(length=16, service="test_service", username="test_user")
        password.save_pw()
        mock_save_pass.assert_called_once_with("test_user", "test_service", password.password)