import time
from unittest.mock import patch
from pwtool.models import App

# Test for App class
def test_app_login_success():
    with patch("models.MasterKeyManager.verify_master_key", return_value=True):
        app = App(timeout_minutes=5)
        app.hashed_master_key = "mock_hashed_key"
        result, masterkey = app.login("test_password")
        assert result is True
        assert app.logged_in is True
        assert app.masterkey == "test_password"

def test_app_login_failure():
    with patch("models.MasterKeyManager.verify_master_key", return_value=False):
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
    assert app.is_session_active() is False

def test_app_logout():
    app = App(timeout_minutes=5)
    app.logged_in = True
    app.logout()
    assert app.logged_in is False
    assert app.last_active is None