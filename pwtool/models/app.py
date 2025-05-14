from auth import MasterKeyManager 
from utils import get_hashed_masterkey 
from storage import get_masterkey
import time

class App:
    def __init__(self,  timeout_minutes=5):
        self.masterkey_manager = MasterKeyManager()
        self.timeout = timeout_minutes * 60
        self.last_active = None
        self.logged_in = False
        self.hashed_master_key = get_masterkey()
        
    
    def login(self, password ):
        if self.masterkey_manager.verify_master_key(self.hashed_master_key, password):
           self.logged_in = True
           self.last_active = time.time()
           print("\nlogin successful\n")
           self.masterkey = password
           return True, self.masterkey 
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