import sys
import time
try:
    import colorama
    import pyfiglet
    from InquirerPy import inquirer
    from InquirerPy.base.control import Choice
except ImportError:
    import subprocess
    print("colorama not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    import colorama
from models import Password
from storage import view_pass, edit_pass, delete_pass

def generate_and_save_password():
        a = Password()
        print(f"length of your password: {a.length}\n")
        print("Generated password:")
        print(colorama.Fore.MAGENTA + a.password)
        sys.stdout.write(colorama.Style.RESET_ALL)
        print("\nyou can now copy your password, keep it safe")
        a.save_pw()

def exit_app():
    print(colorama.Fore.RED, "Closing pwtool...", colorama.Fore.RESET)
    time.sleep(1)
    sys.exit(0)

def get_username_and_service():
    username = inquirer.text(message="Enter username:").execute()
    service = inquirer.text(message="Enter the service:").execute()
    return username, service

def main():
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
    ).execute()

    if action == "Exit":
       exit_app() 

    if action == "Generate password":
       generate_and_save_password()

    if action == "View password":
            username, service = get_username_and_service() 
            view_pass(username, service)
        
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
        edit_pass(username, service, option=action)

    if action == "Delete password":
        username, service = get_username_and_service()
        delete_pass(username, service) 

if __name__ == "__main__":
    pwtool = pyfiglet.figlet_format("pwtool")
    print("\n", colorama.Fore.BLUE + pwtool + colorama.Fore.RESET)
    print("pwtool is a CLI utility for managing passwords.")

    while True:
        try:
            main() 
        except KeyboardInterrupt as e:
            exit_app() 