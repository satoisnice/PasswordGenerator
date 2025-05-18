import base64, os

from InquirerPy import inquirer
from pathlib import Path
from pwtool.storage import store_masterkey, store_salt, get_salt

from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet, InvalidToken
import base64
import os
from pathlib import Path
# from storage import store_masterkey, store_salt, get_salt
from InquirerPy import inquirer
import colorama, keyring

class MasterKeyManager():
    def __init__(self):
        self.ph = PasswordHasher()
    
    def derive_master_key(self, password):
        return self.ph.hash(password)

    def verify_master_key(self, stored_hash, password):
        try:
            self.ph.verify(stored_hash, password)
            return True
        except Exception as e:
            print("something went wrong:", e)
            return False


def derive_fernet_key_argon2(password, salt):
    password_bytes = password.encode()

    key = hash_secret_raw(
        secret=password_bytes,
        salt=salt,
        time_cost=3, #2 seems to be standard. time_cost is number of times algo will be computed.
        memory_cost=131072, #128 MB
        parallelism=4,
        hash_len=32, # length of bytes, fernet requires 32
        type=Type.ID # Type.I resistant to side-channel attacks? Type.D resistant to GPU/ASIC brute-force. Type.ID is balance of both.
    )

    return base64.b64encode(key)

def initial_setup_password(password=None):
    manager = MasterKeyManager()

    password = keyring.get_password("pwtool", "admin")
    if password:
        print("Master password already set.")
        confirm = inquirer.confirm(
            message="Would you like to overwrite the master password?"
        ).execute()
        if confirm:
            new_pass = input("Enter new master password: ")
            hashed_pw = manager.derive_master_key(new_pass)
            store_masterkey(hashed_pw)

    else:
        if password is None:
            password = input("Create a master password: ")
        hashed_pw = manager.derive_master_key(password)
        store_masterkey(hashed_pw)
        print("Master password set.\n")

def initial_setup_salt():
    salt_file = Path("salt.bin")
    if salt_file.exists() and salt_file.stat().st_size > 0:
        print("Salt already set.")
        salt = get_salt()

    else:
        salt = os.urandom(16)
        store_salt(salt)
        print("Salt created and saved.")

def encrypt(master_password: str, password: str, salt: bytes):    
    password_bytes = password.encode()
    key = derive_fernet_key_argon2(master_password, salt)
    f = Fernet(key)
    return f.encrypt(password_bytes)

def decrypt(master_password: str, encrypted_password_bytes: bytes, salt: bytes):
    key = derive_fernet_key_argon2(master_password, salt)
    f = Fernet(key)

    try:
        decrypted_bytes = f.decrypt(encrypted_password_bytes)
    except TypeError:
        print(f"{colorama.Fore.RED}WARNING:{colorama.Style.RESET_ALL} Expected bytes, password is likely base64 encoded. Please update your password entry.")
        return encrypted_password_bytes
    except InvalidToken: 
        print(f"\n{colorama.Fore.RED}WARNING: {colorama.Style.RESET_ALL}Decryption failed. Possibly wrong master password or corrupted data.\n")
        return encrypted_password_bytes
    
    try:
        return decrypted_bytes.decode("utf-8")
    except Exception as e:
        print(f"\n{colorama.Fore.RED}WARNING: {colorama.Style.RESET_ALL}Decryption failed. Possibly wrong master password or corrupted data.\n")
        print(e)
        return None
