import random, csv, time

from pathlib import Path
from pwtool.utils import is_valid_char,get_hashed_masterkey
from pwtool.auth import MasterKeyManager, encrypt, decrypt
from pwtool.storage import get_masterkey,get_salt, save_pass

from argon2 import PasswordHasher
from cryptography.fernet import Fernet

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
        username, service = "",""
        while True:
            if username == "":
                username = input("Enter username:\n")
            elif service == "":
                service = input("For which service is this password for?\n")
            else:
                try:
                    pw_len = int(input("Type desired length of the password (16 character minimum):"))
                    if pw_len < 16:
                        print("Password must be at least 16 characters. For more information about password security: https://bitwarden.com/blog/how-long-should-my-password-be/")
                    else:
                        return pw_len, service, username
                except ValueError as e:
                    print("Enter a valid number for password length", e)

    def gen_pw(self):
        if self.length < 4:
            raise ValueError("To include all categories password must be of length 4 or greater")

        password = [
            random.choice(UPPERCASE),
            random.choice(LOWERCASE),
            random.choice(DIGITS),
            random.choice(SPECIAL_CHARACTERS)
        ]

        fill_in_length = self.length - len(password)
        all_chars = UPPERCASE + LOWERCASE + DIGITS + SPECIAL_CHARACTERS

        for _ in range(fill_in_length):
            password += [random.choice(all_chars)]
        
        random.shuffle(password)

        valid_password = []
        for char in password:
            if is_valid_char(char):
                valid_password.append(char)

        while len(valid_password) < self.length:
            valid_password.append(random.choice(all_chars)) 

        random.shuffle(valid_password)

        return ''.join(valid_password)
    
    def save_pw(self):
        save_pass(self.username, self.service, self.password)
