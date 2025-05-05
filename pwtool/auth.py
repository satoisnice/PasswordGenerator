from argon2 import PasswordHasher

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