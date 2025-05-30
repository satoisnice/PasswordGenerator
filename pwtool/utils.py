from pathlib import Path
import pyperclip, colorama

def is_valid_char(c):
    return c.isprintable() and c not in "\n\r\t\x0b\x0c"

# len("\n") == 1

def get_hashed_masterkey():
    file_path = Path("master.hash")
    try:
        if file_path.is_file():
            with open(file_path, "r") as file:
                return file.readline()
        else:
            print("master.hash doesnt exist. Please create")
    except Exception as e:
        print(e)

import getpass

def prompt_master_password():
    from pwtool.auth import MasterKeyManager
    manager = MasterKeyManager()
    for attempt in range(3):
        master_pass = getpass.getpass("Enter master password: ")
        if manager.verify_master_key(master_pass):
            return master_pass
        else:
            print("Incorrect master password. Try again.")
    print("Too many failed attempts. Aborting.")
    return None

def copy(password):
    try:
        pyperclip.copy(password)
        print(f"{colorama.Fore.GREEN}Password copied to clipboard") # Chagne to auto copy to clipboard
    except Exception:
        print("Error copying to clipboard, Linux requires a clipboard system such as xclip for this feature to work.")
