from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type
import base64
from pathlib import Path

def derive_master_key(password):
    return PasswordHasher.hash(password)

def verify_master_key(stored_hash, password):
    try:
        PasswordHasher.verify(stored_hash, password)
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

def initial_setup(password=None):
    salt_exists = False
    master_exists = False
    salt_is_blank = True
    master_is_blank = True

    if Path("master.hash").exists():
        master_exists = True
        try:
            with open("master.hash", "r") as m_hash_file:
                if m_hash_file.read() == "":
                    print("master.hash file exists but no master key exists.")

                else:
                    master_is_blank = False
                    print("master key already setup.")
        except FileNotFoundError as e:
            
    