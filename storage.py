import csv
import colorama
from models import Password

def view_pass(username, service):
    '''
    Takes a username and service and returns a password from passwords.csv

            Parameters:
                    username (string): A username for some service
                    service  (string): The service (gmail, icloud, etc..)
            Returns:
                    profile['password'] (str): String containing the password matching the username and service.
    '''
    with open("passwords.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["service"] == service:
                profile = {
                    "service": row["service"],
                    "username": row["username"],
                    "password": row["password"] 
                }
                print(f"Service: {colorama.Fore.MAGENTA + profile['service']}\n{colorama.Style.RESET_ALL}Username: {colorama.Fore.MAGENTA + profile['username']}\n{colorama.Style.RESET_ALL}Password: {colorama.Fore.MAGENTA + profile['password']} {colorama.Style.RESET_ALL}")
                return profile['password']
    print(f"No password with username: {username} and service: {service} found")
    return None

def edit_pass(username, service, option="autogenerate"):
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
    # This will take the username and service of the user and give them a string.
    with open("passwords.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['service'] == service:
                print(f"Current password: {row['password']}")
                if option == "userinput":
                    #prompt the user to enter a new password
                    new_pass = input("Type in your new password: ")
                else:
                    temp_pw_obj = Password(username=username, service=service)
                    new_pass = temp_pw_obj.password
                    print(f"Your new password is: {colorama.Fore.MAGENTA}{new_pass}{colorama.Fore.RESET}\nKeep it safe.")
                # change the password value to the new one
                row["password"] = new_pass
            else:
                print(f" username: {username} and service: {service} was not found.")
                return
            # append the updated values
            new_rows.append(row)

    # actually edit the value
    with open("passwords.csv", 'w', newline='') as file2:
        writer = csv.DictWriter(file2, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    # let the user know the password changed
    print("Password successfully changed")