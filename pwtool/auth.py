from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type
import base64

class MasterKeyManager:
    def __init__(self):
        self.ph = PasswordHasher()
        self.hashed_master_key = None

    def derive_master_key(self, password):
        self.hashed_master_key = self.ph.hash(password)

        return self.hashed_master_key

    def verify_master_key(self, stored_hash, password):
        try:
            self.ph.verify(stored_hash, password)
            return True
        except Exception as e:
            print("something went wrong:", e)
            return False

    def return_stored_hash(self):
        return self.hashed_master_key

def derive_fernet_key_argon2(password, salt):
    password_bytes = password.encode()

    key = hash_secret_raw(
        secret=password_bytes,
        salt=salt,
        time_cost=3, #2 seems to be standard. time_cost is number of times algo will be computed.
        memory_cost=131072, #128 MB
        parallelism=4,
        hash_len=32, # length of bytes, fernet requires 32
        type=Type.ID
    )

    return base64.b64encode(key)