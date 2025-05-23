import sys, time, threading, threading, getpass, subprocess, json, base64, os
from pathlib import Path
try:
    import colorama, pyfiglet
    from InquirerPy import inquirer, get_style
    from InquirerPy.base.control import Choice
except ImportError:
    import subprocess
    print("colorama not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    import colorama
from pwtool.models.app import App
from pwtool.models.password import Password
from pwtool.storage import view_pass, edit_pass, delete_pass, save_pass, get_salt, get_masterkey, read_json_file, b64_decode, b64_encode, write_json_file
from pwtool.auth import initial_setup_password, initial_setup_salt, encrypt, decrypt, encrypt_content, decrypt_content
from pwtool.constants.paths import PASS_FILE, SALT_FILE
from pwtool.utils import copy

PASS_FILE = Path("passwords.json")
AGE_PASS_FILE = Path("passwords.json.age")

style = get_style({
    "questionmark": "#ff8000",
    "answermark": "#e5c07b",
    "answer": "#61afef",
    "input": "#98c379",
    "question": "",
    "answered_question": "",
    "instruction": "#abb2bf",
    "long_instruction": "#abb2bf",
    "pointer": "#61afef",
    "checkbox": "#98c379",
    "separator": "",
    "skipped": "#5c6370",
    "validator": "",
    "marker": "#e5c07b",
    "fuzzy_prompt": "#c678dd",
    "fuzzy_info": "#abb2bf",
    "fuzzy_border": "#4b5263",
    "fuzzy_match": "#c678dd",
    "spinner_pattern": "#e5c07b",
    "spinner_text": "",
                   })

def encrypt_with_age():
    subprocess.run

def generate_and_save_password():
    a = Password()
    if (view_pass(a.username, a.service)) != None:
        print(f"\nEntry already exists for username: {a.username} and service: {a.service}")
        print("If you want to change this password please use the edit option\n")
        return
    print(f"length of your password: {a.length}\n")
    print("Generated password:")
    print(colorama.Fore.MAGENTA + a.password)
    sys.stdout.write(colorama.Style.RESET_ALL)
    copy(a.password) 
    pw_salt = get_salt("passwords")
    encrypted_pass = encrypt(a.password, pw_salt, key=app.passwords_key)
    save_pass(a.username, a.service, encrypted_pass)

def update_password(username, service, masterkey, option="autogenerate"):
    pw_salt = get_salt("passwords")
    data = read_json_file(PASS_FILE)

    for entry in data:
        if entry["username"] == username and entry["service"] == service:
            current_pw = decrypt(b64_decode(entry["password"]), pw_salt, key=app.passwords_key)
            print(f"Current password: {colorama.Fore.MAGENTA}{current_pw}{colorama.Style.RESET_ALL}")
            break
    else:
        print("No matching entry found")
        
    if option == "userinput":
        new_pw = input("Type your new password: ")
        if new_pw == "":
            print("No changes made.")
            return
    
    else:
        from pwtool.models.password import Password
        new_pw = Password(username=username, service=service).password
        print(f"Your new password is: {colorama.Fore.MAGENTA}{new_pw}{colorama.Style.RESET_ALL}")
    copy(new_pw)
    encrypted_new_pw = encrypt(new_pw, pw_salt, key=app.passwords_key)
    edit_pass(username, service, encrypted_new_pw)


def get_and_view_password(username, service):
    profile = view_pass(username, service)
    if profile == None:
        print(f"No password with username: {username} and service: {service} found")
        return None
    password = profile["password"]
    salt = get_salt("passwords")
    pw = decrypt(password, salt, key=app.passwords_key)
    try:
        print(f"""
    Service: {colorama.Fore.MAGENTA + username + colorama.Style.RESET_ALL}
    Username: {colorama.Fore.MAGENTA + service + colorama.Style.RESET_ALL}
    Password: {colorama.Fore.MAGENTA + pw + colorama.Style.RESET_ALL}
    """)
    except TypeError:
        print(f"{colorama.Fore.RED}ERROR: {colorama.Style.RESET_ALL}login password changed please update your password entries.")
    copy(pw)
    
def view_all():
    try:
        data = read_json_file(PASS_FILE) 
        for entry in data:
            password_b64 = entry["password"]
            password_bytes = b64_decode(password_b64)
            salt = get_salt("passwords")
            pw = decrypt(password_bytes, salt, key=app.passwords_key)
            print(f"""{"username:" + colorama.Fore.BLUE + entry["username"] + colorama.Style.RESET_ALL}\n{"service:" + colorama.Fore.BLUE + entry["service"] + colorama.Style.RESET_ALL}
Password:{colorama.Fore.MAGENTA + pw + colorama.Style.RESET_ALL}\n""")
    except FileNotFoundError:
        print("passwords.json not found")
        return None

def backup_data(file_path, key):
    try:
        key = base64.urlsafe_b64decode(key)
        data = read_json_file(file_path)

        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        nonce, encrypted_data = encrypt_content(key, data)
        # print("encrypted_data:", encrypted_data)
        # print("b64 encrypted_data", b64_encode(encrypted_data))
        encrypted_data = {
            "nonce": b64_encode(nonce),
            "ciphertext": b64_encode(encrypted_data)
        }
        return encrypted_data
    except Exception as e:
        print("Error encrypting and storing files", e)



def decrypt_backup(file_path, key, name):
        key = base64.urlsafe_b64decode(key)
        data = read_json_file(file_path)
        combined = {}
        print(name)
        for entry_name, entry in data.items():
            
            nonce = b64_decode(entry["nonce"])
            print("decryption nonce", nonce)
            ciphertext = b64_decode(entry["ciphertext"])
            decrypted_data = decrypt_content(key, nonce, ciphertext)
            decrypted_str = decrypted_data.decode("utf-8")
            try:
                decrypted_json = json.loads(decrypted_str)
            except json.JSONDecodeError:
                print("erro1")
                decrypted_json = decrypted_str
            
            combined[entry_name] = decrypted_json
            print(decrypted_json)
            if name == "salt":
                write_json_file(SALT_FILE, decrypted_json, mode="w")
            elif name == "passwords":
                if isinstance(decrypted_json, (dict, list)):
                    write_json_file(PASS_FILE, decrypted_json, mode="w")
                else:
                    with open(PASS_FILE, "w") as f:
                        f.write(decrypted_json)

        write_path = Path("backup.unenc") 
        write_json_file(write_path, combined, mode="w")

def exit_app():
    print(colorama.Fore.RED, "Closing pwtool...", colorama.Fore.RESET)
    time.sleep(1)
    try:
        if app.logged_in:
            encrypted_data = { 
                "passwords": backup_data(PASS_FILE, app.files_key)
            }
            # print("app.files_key = ", app.files_key)
            write_json_file("backup.enc", encrypted_data) 
            # if os.path.exists(PASS_FILE):
            #     os.remove(PASS_FILE) 
            # if os.path.exists(SALT_FILE):
                # os.remove(SALT_FILE)
        app.passwords_key = None
        app.files_key = None
        app.logout()
    except Exception as e:
        print(e)
        sys.exit(0)
    sys.exit(0)

def get_username_and_service():
    username = inquirer.text(message="Enter username:",validate=lambda result: len(result) > 0,invalid_message="Input cannot be empty.").execute()
    service = inquirer.text(message="Enter the service:",validate=lambda result: len(result) > 0,invalid_message="Input cannot be empty.").execute()
    return username, service

def session_tracker(app):
    while True:
        time.sleep(1)
        if app.logged_in==False and not app.is_session_active():
            print("Session expired. Please log in again.")
            app.login(input("Your password:"))

def main(app):
    threading.Thread(target=session_tracker, args=(app,), daemon=True).start()

    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Generate password",
            "View password",
            "View all",
            "Edit password",
            "Delete password",
            "Exit"
        ],
        default="Select password",
        style=style

    ).execute()

    if action == "Exit":
        exit_app() 

    if not app.is_session_active():
        print("session expired. please login again")
        return

    if action == "Generate password":
        generate_and_save_password()

    if action == "View password":
        username, service = get_username_and_service() 
        # view_pass(username, service)
        get_and_view_password(username, service)

    if action == "View all":
        view_all()    
    
    if action == "Edit login password":
        initial_setup_password()
        
    if action == "Edit password":
        username, service = get_username_and_service()  
        action = inquirer.select(
            message="Select action",
            choices=[
                Choice(name="Autogenerate password", value="autogenerate"),
                Choice(name="Input password", value="userinput")
            ]
        ).execute()
        update_password(username, service, app.passwords_key, option=action)

    if action == "Delete password":
        username, service = get_username_and_service()
        confirm_delete = inquirer.confirm(message=f"Are you sure you want to delete the password for '{username}'? It cannot be recovered.").execute()
        if confirm_delete == True:
            delete_pass(username, service)

    app.active()        

if __name__ == "__main__":
    try:
        pwtool = pyfiglet.figlet_format("pwtool")
        print("\n", colorama.Fore.BLUE + pwtool + colorama.Fore.RESET)
        print("pwtool is a CLI utility for managing passwords.")
        print(f"{colorama.Fore.YELLOW}CTRL + C {colorama.Fore.RESET}to close pwtool at any time.\n")
        try:
            if get_masterkey() == None:
                initial_setup_password()
            # print("salt check", get_salt())
            if get_salt() == None:
                initial_setup_salt()


            app = App()
        except KeyboardInterrupt as e:
            exit_app()

        while True:
            if not app.is_session_active():
                while True:
                    master_pass = getpass.getpass("Your password:")
                    if app.login(master_pass):
                        master_pass = None
                        # decrypt_backup(Path("backup.enc"), app.files_key, "passwords")
                        break
                    print("incorrect password. Try again")
            try:
                main(app) 
            except KeyboardInterrupt as e:
                exit_app() 
    except KeyboardInterrupt as e:
        exit_app()