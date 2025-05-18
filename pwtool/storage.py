import colorama, keyring, json, base64
from pathlib import Path
from pwtool.utils import prompt_master_password

PASS_FILE = Path("passwords.json")

# helper functions
def b64_encode(encrypted_bytes):
    """encode encrypted bytes to b64 string for storage"""
    return base64.b64encode(encrypted_bytes).decode("utf-8")

def b64_decode(encoded_str):
    """decode b64 string to encrypted bytes"""
    return base64.b64decode(encoded_str)

def read_json_file(path):
    if not path.is_file():
        return []
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []

def write_json_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def save_pass(username, service, password_bytes):
    data = read_json_file(PASS_FILE)

    encoded_password = b64_encode(password_bytes)

    data.append({
        "username": username,
        "service": service,
        "password": encoded_password
    })

    write_json_file(PASS_FILE, data)


def view_pass(username, service):
    '''
    Takes a username and service and returns a password from passwords.json

            Parameters:
                    username (string): A username for some service
                    service  (string): The service (gmail, icloud, etc..)
            Returns:
                    profile['password'] (str): String containing the password matching the username and service.
    '''
    data = read_json_file(PASS_FILE) 
    for entry in data:
        if entry["username"] == username and entry["service"] == service:
            entry["password"] = b64_decode(entry["password"])
            return entry

    print(f"No password with username: {username} and service: {service} found")
    return None


def edit_pass(username, service, new_password_bytes):
    data = read_json_file(PASS_FILE)
    found = False

    for entry in data:
        if entry["username"] == username and entry["service"] == service:
            found = True
            entry["password"] = b64_encode(new_password_bytes)
            break
    
    if not found:
        print(f"username: {username} and service: {service} was not found.")
        return False
    
    write_json_file(PASS_FILE, data)
    print("Password successfully changed")
    return True


def delete_pass(username, service):
    data = read_json_file(PASS_FILE)
    new_data = []
    for entry in data:
        if entry["password"] != username and entry ["service"] != service:
            new_data.append(entry)
    
    if len(new_data) == len(data):
        print(f"username: {username} and service: {service} was not found")
        return
    
    write_json_file(PASS_FILE, new_data)
    print("Password successfully deleted\n")


def store_masterkey(hashed_master_key):
    try:
        keyring.set_password("pwtool", "admin", hashed_master_key)
    except Exception as e:
        print(e)
        return


def get_masterkey():
    try:
        password = keyring.get_password("pwtool", "admin")
        if password:
            return keyring.get_password("pwtool", "admin")
        else:
            print("login password not set")
            return None
    except Exception as e:
        print(e)
        return

def delete_masterkey():
    try:
        password = keyring.get_password("pwtool", "admin")
        if password:
            keyring.delete_password("pwtool", "admin")
            print("Master password successfully deleted.")
            return
        else:
            print("master password does not exist")
    except Exception as e:
        print(e)
        return

def store_salt(salt):
    file_path = Path("salt.bin")
    try:
        if file_path.is_file():
            with open(file_path, "wb") as f:
                f.write(salt)
        else:
            file_path.touch(exist_ok=True)
            with open(file_path, "wb") as file:
                file.write(salt)
    except Exception as e:
        return e


def get_salt():
    file_path = Path("salt.bin")
    try:
        if file_path.is_file():
            with open(file_path, "rb") as file:
                return file.read()
        else:
            return None
    except Exception as e:
        print(e)
        return