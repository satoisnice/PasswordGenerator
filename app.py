import sys
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
from storage import view_pass, edit_pass

def main():
    pwtool = pyfiglet.figlet_format("pwtool")
    print("\n", colorama.Fore.BLUE + pwtool + colorama.Fore.RESET)
    print("pwtool is a CLI utility for managing passwords.")
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Generate password",
            "Select password",
            Choice(value=None, name="Exit"),
        ],
        default="Select password",
    ).execute()

    if action == "Generate password":
        a = Password()
        print(f"length of your password: {a.length}\n")
        print("Generated password:")
        print(colorama.Fore.MAGENTA + a.password)
        sys.stdout.write(colorama.Style.RESET_ALL)
        print("\nyou can now copy your password, keep it safe")
        a.save_pw()

    if action == "Select password":
        action2 = inquirer.select(
            message="Select action:",
            choices=[
                "View password",
                "Edit password",
                Choice(value="exec del_pw", name="Delete password")
            ],
        ).execute() 
        if action2 == "View password":
            username = inquirer.text(message="Enter username:").execute()
            service = inquirer.text(message="Enter the service:").execute()
            view_pass(username, service)
        
        if action2 == "Edit password":
            username = inquirer.text(message="Enter username:").execute()
            service = inquirer.text(message="Enter the service:").execute()
            # print statement to show the output
            edit_pass(username, service)

        if action2 == "Delete password":
            #To-Do

            pass
        

if __name__ == "__main__":
    try:
        main() 
    except KeyboardInterrupt as e:
        print(colorama.Fore.RED, "Closing pwtool", colorama.Fore.RESET)