import random
import csv
from pathlib import Path

UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Uppercase letters
LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'  # Lowercase letters
DIGITS = '0123456789'  # Numbers
SPECIAL_CHARACTERS = '!@#$%^&*()_+-={}[]|:;\"\'<>,.?/~`'  # Special characters
FIELD_NAMES = "username","service","password"
CHARACTERS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',  # Uppercase letters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',  # Lowercase letters
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  # Digits
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '-', '{', '}', '[', ']', '|', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '~' # Special characters
]


class Password:
    '''
    A class to represent a password.

    ...

    Attributes
    ----------
    length: int
        length of the password 
    service: str
        the service the password is used for
    username: str
        the username the password is used for
    password: str
        a password
    
    Methods
    -------
    get_inputs():
        obtains length, service, and username from the user
    gen_pw():
        returns a randomly generated password based on length
    save_pw():
        saves password to passwords.csv file
    
    '''
    def __init__(self, length=16, service=None, username=None):
        if length is None or service is None or username is None:    
            self.length, self.service, self.username =  self.get_inputs()
        else:
            self.length = length
            self.service = service
            self.username = username 
            
        self.password = self.gen_pw() 

    def get_inputs(self):
        while True:
            try:
                username = input("Enter username:\n")
                service = input("For which service is this password for?\n")
                pw_len = int(input("Type desired length of the password (8 character minimum):"))
                if pw_len < 8:
                    print("Password must be at least 8 characters.")
                else:
                    return pw_len, service, username
            except ValueError as e:
                print("Enter a valid number for password length")

    def gen_pw(self):
        password = "".join(random.choice(CHARACTERS) for _ in range(self.length))
        return password
    
    def save_pw(self):
        pass_file = Path("passwords.csv")
        if pass_file.is_file():
            with open(pass_file, 'a') as file:
                data = csv.writer(file)
                data.writerow([self.username, self.service, self.password])

        else:
            pass_file.touch(exist_ok=True)
            with open(pass_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["username", "service", "password"])
                writer.writerow([self.service, self.username, self.password])