from pwtool.auth import MasterKeyManager, derive_fernet_key_argon2, derive_subkey
from pwtool.utils import get_hashed_masterkey 
from pwtool.storage import get_masterkey, get_salt
import time, colorama

class App:
    def __init__(self,  timeout_minutes=5):
        self.masterkey_manager = MasterKeyManager()
        self.timeout = timeout_minutes * 60
        self.last_active = None
        self.logged_in = False
        self.argon2_key = get_masterkey()
        self.hashed_master_key = None
        self.passwords_key = None
        self.files_key = None
        
    
    def login(self, password ):
        if self.masterkey_manager.verify_master_key(self.argon2_key, password):
           self.logged_in = True
           self.last_active = time.time()
           print(f"\n{colorama.Fore.GREEN}login successful{colorama.Fore.RESET}\n")

           base_salt = get_salt("base") 
           self.hashed_master_key = derive_fernet_key_argon2(self.argon2_key, base_salt) 
           pw_salt = get_salt("passwords")
           self.passwords_key = derive_subkey(self.hashed_master_key, pw_salt, "passwords")
           files_salt = get_salt("files")
           self.files_key = derive_subkey(self.hashed_master_key, files_salt, "files")
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