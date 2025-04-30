import csv
import colorama

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

def edit_pass(username, service):
    # the updated rows
    new_rows = []
    # This will take the username and service of the user and give them a string.
    with open("passwords.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['service'] == service:
                print(f"Current password: {row['password']}")
                #prompt the user to enter a new password
                new_pass = input("Type in your new password: ")
                # change the password value to the new one
                row["password"] = new_pass
            else:
                print(f" username: {username} and service: {service} was not found.")
            # append the updated values
            new_rows.append(row)
    # actually edit the value
    with open("passwords.csv", 'w', newline='') as file2:
        writer = csv.DictWriter(file2, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    # let the user know the password changed
    print("Successfully changed")