from pwtool.auth import MasterKeyManager, derive_fernet_key_argon2 
from pwtool.utils import get_hashed_masterkey 
from pwtool.storage import get_masterkey, get_salt
import time

class App:
    def __init__(self,  timeout_minutes=5):
        self.masterkey_manager = MasterKeyManager()
        self.timeout = timeout_minutes * 60
        self.last_active = None
        self.logged_in = False
        self.hashed_master_key = get_masterkey()
        self.derived_key = None
        
    
    def login(self, password ):
        if self.masterkey_manager.verify_master_key(self.hashed_master_key, password):
           self.logged_in = True
           self.last_active = time.time()
           print("\nlogin successful\n")
           salt = get_salt()
           self.derived_key = derive_fernet_key_argon2(password, salt)
           return True 
        else:
           return False

    def is_session_active(self):
        if not self.logged_in:
            return False
        if time.time() - self.last_active > self.timeout:
            self.logged_in = False
            return False
        return True

    def active(self):
        if self.logged_in:
            self.last_active = time.time()
    
    def logout(self):
        self.logged_in = False
        self.last_active = None