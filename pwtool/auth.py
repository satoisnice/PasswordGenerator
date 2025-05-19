import base64, os, colorama, keyring

from InquirerPy import inquirer
from pathlib import Path
from pwtool.storage import store_masterkey, store_salts, get_salt
from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os
from pathlib import Path
# from storage import store_masterkey, store_salt, get_salt
from InquirerPy import inquirer
import colorama, keyring
from pwtool.constants.paths import SALT_FILE

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


def derive_fernet_key_argon2(password, salt): #should be reanamed to derive_master_key but would be a hassle to change
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

def derive_subkey(base_key: bytes, salt: bytes, content: str) -> bytes:
    key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=content.encode(),
        backend=default_backend()
    ).derive(base_key)

    return base64.urlsafe_b64encode(key)

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
    salts = get_salt
    if SALT_FILE.exists() and SALT_FILE.stat().st_size > 0:
        print("Salt already set.")
        salt_dict = get_salt()
        passwords_salt = salt_dict["passwords_salt"]
        files_salt = salt_dict["files_salt"]
        base_salt = salt_dict["base_salt"]
    else:
        passwords_salt = os.urandom(16)
        files_salt = os.urandom(16)
        base_salt = os.urandom(16)
        salts = {
            "base_salt": base_salt,
            "passwords_salt": passwords_salt,
            "files_salt": files_salt
        }
        store_salts(salts)
        print("Salt created and saved.")
    return passwords_salt, files_salt 


def encrypt(password: str, salt: bytes, master_password: str = None, key: bytes = None):    
    if key is None:
        key = derive_fernet_key_argon2(master_password, salt)
    password_bytes = password.encode()
    f = Fernet(key)
    return f.encrypt(password_bytes)

def decrypt(encrypted_password_bytes: bytes, salt: bytes, master_password: str = None, key: bytes = None):
    if key is None:
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

def encrypt_content(key: bytes, content):
    if isinstance(content, str):
        content_bytes = content.encode()
    else:
        content_bytes = content

    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm .encrypt(nonce, content_bytes, None)
    return nonce, ciphertext

def decrypt_content(key: bytes, nonce: bytes, ciphertext: bytes):
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)