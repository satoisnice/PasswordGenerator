import time
from unittest.mock import patch
from pwtool.models.app import App

# Test for App class
def test_app_login_success():
    mock_password = "test_password"
    mock_hashed_key = "mock_hashed_key"
    mock_derived_key = b"mock_derived_key_bytes"
    mock_salt = b"mock_salt"

    with patch("pwtool.models.password.MasterKeyManager.verify_master_key", return_value=True), \
        patch("pwtool.app.get_salt", return_value=mock_salt), \
        patch("pwtool.models.app.derive_subkey", return_value=mock_derived_key): 

        app = App(timeout_minutes=5)
        app.hashed_master_key = mock_hashed_key
        app.argon2_key = mock_password
        
        result = app.login(mock_password)

        assert result is True
        assert app.logged_in is True
        assert app.passwords_key == mock_derived_key

def test_app_login_failure():
    with patch("pwtool.models.password.MasterKeyManager.verify_master_key", return_value=False):
        app = App(timeout_minutes=5)
        app.hashed_master_key = "mock_hashed_key"
        result = app.login("wrong_password")
        assert result is False
        assert app.logged_in is False

def test_app_session_active():
    app = App(timeout_minutes=5)
    app.logged_in = True
    app.last_active = time.time()
    assert app.is_session_active() is True

def test_app_session_timeout():
    app = App(timeout_minutes=5)
    app.logged_in = True
    app.last_active = time.time() - 3600  # Simulate 1 hour of inactivity
    # test
    assert app.is_session_active() is False

def test_app_logout():
    app = App(timeout_minutes=5)
    app.logged_in = True
    app.logout()
    assert app.logged_in is False
    assert app.last_active is None