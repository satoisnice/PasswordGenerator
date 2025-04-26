import random
import sys
try:
    import colorama
except ImportError:
    import subprocess
    print("colorama not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    import colorama

CHARACTERS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',  # Uppercase letters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',  # Lowercase letters
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  # Digits
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '-', '{', '}', '[', ']', '|', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/', '~' # Special characters
]

class Password:
    def __init__(self):
        self.length =  self.get_inputs()
        self.password = self.genPW() 

    def get_inputs(self):
        while True:
            try:
                pw_len = int(input("Type desired length of the password (8 character minimum):"))
                if pw_len < 8:
                    print("Password must be at least 8 characters.")
                else:
                    return pw_len
            except ValueError as e:
                print("Enter a valid number for password length")

    def genPW(self):
        password = "".join(random.choice(CHARACTERS) for _ in range(self.length))
        return password

if __name__ == "__main__":
    a = Password()
    print(f"length of your password: {a.length}\n")
    print("Generated password:")
    print(colorama.Fore.MAGENTA + a.password)
    sys.stdout.write(colorama.Style.RESET_ALL)
    print("\nyou can now copy your password, keep it safe i aint saving it")