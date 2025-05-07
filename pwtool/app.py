import sys, time, threading

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

from models import Password, App
from storage import view_pass, edit_pass, delete_pass, get_salt, save_pass
from auth import initial_setup, encrypt, decrypt


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

def generate_and_save_password():
        a = Password()
        print(f"length of your password: {a.length}\n")
        print("Generated password:")
        print(colorama.Fore.MAGENTA + a.password)
        sys.stdout.write(colorama.Style.RESET_ALL)
        print("\nyou can now copy your password, keep it safe")
        salt = get_salt()
        encrypted_pass = encrypt(app.masterkey, a.password, salt)
        save_pass(a.username, a.service, encrypted_pass)

def get_and_view_password(username, service):
    profile = view_pass(username, service)
    password = profile["password"]
    salt = get_salt()
    pw = decrypt(app.masterkey, password, salt)
    print(f"Service: {colorama.Fore.MAGENTA + username}\n{colorama.Style.RESET_ALL}Username: {colorama.Fore.MAGENTA + service}\n{colorama.Style.RESET_ALL}Password: {colorama.Fore.MAGENTA + pw} {colorama.Style.RESET_ALL}")
    


def exit_app():
    print(colorama.Fore.RED, "Closing pwtool...", colorama.Fore.RESET)
    time.sleep(1)
    app.logout()
    sys.exit(0)

def get_username_and_service():
    username = inquirer.text(message="Enter username:").execute()
    service = inquirer.text(message="Enter the service:").execute()
    return username, service

def session_tracker(app):
    while True:
        time.sleep(1)
        if app.logged_in==False and not app.is_session_active():
            print("Session expired. Please log in again.")
            app.login(input("Your password:"))

def main(app):
    master_pass = app.masterkey
    threading.Thread(target=session_tracker, args=(app,), daemon=True).start()

    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Generate password",
            "View password",
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
        
    if action == "Edit password":
        username = inquirer.text(message="Enter username:").execute()
        service = inquirer.text(message="Enter the service:").execute()
        action = inquirer.select(
            message="Select action",
            choices=[
                Choice(name="Autogenerate password", value="autogenerate"),
                Choice(name="Input password", value="userinput")
            ]
        ).execute()
        edit_pass(username, service, master_pass, option=action)

    if action == "Delete password":
        username, service = get_username_and_service()
        confirm_delete = inquirer.confirm(message=f"Are you sure you want to delete the password for '{username}'? It cannot be recovered.").execute()
        if confirm_delete == True:
            delete_pass(username, service)

    app.active()        

if __name__ == "__main__":
    pwtool = pyfiglet.figlet_format("pwtool")
    print("\n", colorama.Fore.BLUE + pwtool + colorama.Fore.RESET)
    print("pwtool is a CLI utility for managing passwords.\n")

    master_path = Path("master.hash")
    if not master_path.exists():
        initial_setup()
    
    app = App()
    
    
    while True:
        if not app.is_session_active():
            while True:
                master_pass = input("Your password:")
                if app.login(master_pass):
                    break
                print("incorrect password. Try again")
        try:
            main(app) 
        except KeyboardInterrupt as e:
            exit_app() 