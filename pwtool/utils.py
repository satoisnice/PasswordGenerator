from pathlib import Path

def is_valid_char(c):
    return c.isprintable() and c not in "\n\r\t\x0b\x0c"

# len("\n") == 1
# hi
#  hihihi

def get_hashed_masterkey():
    file_path = Path("master.hash")
    try:
        if file_path.is_file():
            with open(file_path, "r") as file:
                return file.readline()
        else:
            print("master.hash doesnt exist. Please create")
    except Exception as e:
        print(e)