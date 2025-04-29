import csv

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
            if username or service in row:
                profile = {
                    "service": row["service"],
                    "username": row["username"],
                    "password": row["password"] 
                }
                return profile['password']