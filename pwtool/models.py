import random
import csv
from argon2 import PasswordHasher
from pathlib import Path
from utils import is_valid_char
import time
from datetime import datetime, timedelta
from threading import Event,Thread

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
        username = input("Enter username:\n")
        service = input("For which service is this password for?\n")

        while True:
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
        pass_file = Path("passwords.csv")

        if pass_file.is_file():
            with open(pass_file, 'a', newline='') as file:
                data = csv.writer(file)
                data.writerow([self.username, self.service, self.password])

        else:
            pass_file.touch(exist_ok=True)
            with open(pass_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows([
                    ["username", "service", "password"],
                    [self.username, self.service, self.password]])

from auth import MasterKeyManager
from utils import get_masterkey
import time

class App:
    def __init__(self,  timeout_minutes=1):
        self.masterkey = MasterKeyManager()
        self.timeout = timeout_minutes * 60
        self.last_active = None
        self.logged_in = False
        
    def get_key(self, a="password"):
        self.master_key = get_masterkey() 
    
    def login(self, password ):
        if self.masterkey.verify_master_key(self.master_key, password):
           self.logged_in = True
           self.last_active = time.time()
           return True
        else:
           return False

    def is_session_active(self):
        if not self.logged_in:
            return False
        if time.time() - self.last_active > self.timeout:
            self.logged_in = False
            return False
        return True

    def active(self):
        if self.logged_in:
            self.last_active = time.time()
    
    def logout(self):
        self.logged_in = False
        self.last_active = None

# Timeout class to close session - (time unit is in seconds)
class TimeOut:

    def __init__(self,duration):
        self.duration = duration
        self.future_time = None
        self.event = Event()
        self.thread = None
    
    def start(self):
        # Sets the event flag to false until the set() method sets it to true again.
        self.event.clear()
        # Store the time which the timer needs to countdown.
        self.future_time = datetime.now() + timedelta(seconds=self.duration)

        def run():
            # while the specified time has not yet been reached.
            while datetime.now() < self.future_time:
                # if the event is set (stop event has been triggered) then return (stop execution).
                if self.event.is_set():
                    return
                # wait 1 second while the timer is in execution, this prevents intensive cpu usage.
                time.sleep(1)
        # start a thread for the run function. 
        self.thread = Thread(target=run)
        self.thread.start()

    def stop(self):
        # Trigger the stop function.
        self.event.set()
        # if a thread exists then join it (stop it from executing).
        if self.thread:
            self.thread.join()

    def restart(self):
        self.stop()
        self.start()
    
    def is_running(self):
        if self.event.is_set():
            return False
        return True
    
    def time_over(self):
        while True:
            now = datetime.now()
            countdown = self.future_time - now
            if countdown.total_seconds() <= 0:
                return True
            
    def has_time_over(self):
        return datetime.now() >= self.future_time