from cryptography.fernet import Fernet

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
#    with open("key.key", "wb") as key_file:
    with open("key.key", "a") as key_file:
        key_file.write(str(key) + "\n")
        print("Success : key = " + str(key))
write_key()
print("Success : File saved to disk")
