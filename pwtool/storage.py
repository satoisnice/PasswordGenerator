import csv
import colorama
from models import Password
from pathlib import Path
from auth import encrypt, decrypt

def view_pass(username, service):
    '''
    Takes a username and service and returns a password from passwords.csv

            Parameters:
                    username (string): A username for some service
                    service  (string): The service (gmail, icloud, etc..)
            Returns:
                    profile['password'] (str): String containing the password matching the username and service.
    '''
    try:
        with open("passwords.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["service"] == service:
                    profile = {
                        "service": row["service"],
                        "username": row["username"],
                        "password": decrypt(get_masterkey(), row['password'], get_salt()) 
                    }
                    print(f"""
                          Service: {colorama.Fore.MAGENTA + profile['service']}\n{colorama.Style.RESET_ALL}Username: {colorama.Fore.MAGENTA + profile['username']}\n{colorama.Style.RESET_ALL}Password: {colorama.Fore.MAGENTA + profile['password']} {colorama.Style.RESET_ALL}
                        """)
                    return profile['password']
                print(f"No password with username: {username} and service: {service} found")
                return None
    except FileNotFoundError as e:
        print("passwords.csv not found.")
        return None

def edit_pass(username, service, masterkey, option="autogenerate"):
    from models import Password
    from auth import encrypt, decrypt, MasterKeyManager
    """
    Takes username and service and edits passwords.csv. Edits the password column in a row matching to arguments passed to the function.

            Parameters:
                    username: str
                    username the password is used for
            service: str
                    service the password is used for
            option: str
                    2 options: usergenerate, autogenerate
                    default is autogenerate
    """
    # the updated rows
    new_rows = []
    found = False
    # This will take the username and service of the user and give them a string.
    try:
        with open("passwords.csv", 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row['username'] == username and row['service'] == service:
                    found = True
                    print(f"Current password: {colorama.Fore.MAGENTA}{decrypt(masterkey, row['password'], get_salt())}{colorama.Style.RESET_ALL}")

                    if option == "userinput":
                        #prompt the user to enter a new password
                        new_pass = input("Type in your new password: ")
                        if new_pass == '':
                            print("No changes made to password")
                            return
                    else:   
                        temp_pw_obj = Password(username=username, service=service)
                        new_pass = temp_pw_obj.password
                        print(f"Your new password is: {colorama.Fore.MAGENTA}{new_pass}{colorama.Style.RESET_ALL}")
                        print("Keep it safe.")

            # append the updated values
                    verify = False
                    while not verify:
                        a = MasterKeyManager()
                        prompt_for_master = input("\n To save your new password please enter your login password: ")
                        if a.verify_master_key(get_masterkey(), prompt_for_master):
                            verify = True
                            salt = get_salt()
                            master_pass = prompt_for_master
                            new_pass_encrypted = encrypt(master_pass, new_pass, salt)
                            row["password"] = new_pass_encrypted
                            break
                new_rows.append(row)
            if not found:
                print(f" username: {username} and service: {service} was not found.")
                return

    # actually edit the value
        with open("passwords.csv", 'w', newline='') as file2:
            writer = csv.DictWriter(file2, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)
    # let the user know the password changed

        print("Password successfully changed")
    
    except FileNotFoundError as e:
        print("passwords.csv does not exist", e)
        return

def delete_pass(username, service):
    rows_keep = []
    found = False
    try:
        with open("passwords.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] != username or row["service"] != service:
                    rows_keep.append(row)
                else:
                    found = True
        with open("passwords.csv", "w", newline='') as wrt:
            writer = csv.DictWriter(wrt, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows_keep)
            print("Password successfully deleted")

        if not found:
            print(f"username: {username} and service: {service} was not found.")

    except FileNotFoundError as e:
        print("passwords.csv does not exist", e)
        return
    
def store_masterkey(hashed_master_key, file_path = Path("master.hash")):
    try:
        if file_path.is_file():
            with open(file_path, "w") as f:
                f.write(hashed_master_key)
        else:
            file_path.touch(exist_ok=True)
            with open(file_path, "w") as file:
                file.write(hashed_master_key)
    except Exception as e:
        print(e)
        return

def get_masterkey(file_path = Path("master.hash")):
    try:
        if file_path.is_file():
            with open(file_path, "r") as file:
                return file.read()
        else:
            print("master.hash doesnt exist. Please create")
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
            print("salt.bin doesnt exist. Please create")
    except Exception as e:
        print(e)
        return