vscode-remote://wsl%2Bubuntu/home/harsh_s/random/test/test.py vscode-remote://wsl%2Bubuntu/home/harsh_s/random/test/application.pyimport getpass
from cryptography.fernet import Fernet

# Encrypt the password
def encrypt(password, fernet):
    return fernet.encrypt(password.encode()).decode('utf-8')

# Decrypt the password
def decrypt(encrypted_password, fernet):
    return fernet.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')

# Check if the username exists
def username_exists(username):
    try:
        with open(username + "_passwords.txt", "r") as file:
            return True
    except FileNotFoundError:
        return False

# Sign in function
def sign_in():
    global GLOBAL_USERNAME  # Use the global variable here
    username = input("Enter username: ")

    if username_exists(username):
        print("Username exists")
        password = getpass.getpass("Enter password: ")

        with open(username + "_passwords.txt", "r") as file:
            data = file.readline().split(":")
            key = data[1].encode('utf-8')  # Convert the stored key back to bytes
            encrypted_password = data[2]

        fernet = Fernet(key)
        real_password = decrypt(encrypted_password, fernet)

        if password == real_password:
            GLOBAL_USERNAME = username  # Set the global variable
            print("Access granted")
            return True
        else:
            print("Access denied")
            return False
    else:
        print("Username does not exist")
        return False

# Sign up function
def sign_up():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if username_exists(username):
        print("Username already exists")
        return False

    re_enter_password = getpass.getpass("Re-enter password: ")
    while password != re_enter_password:
        print("Passwords do not match")
        password = getpass.getpass("Enter password: ")
        re_enter_password = getpass.getpass("Re-enter password: ")

    # Generate a new key for this user
    user_key = Fernet.generate_key()
    fernet = Fernet(user_key)

    # Encrypt the password
    encrypted_password = encrypt(password, fernet)

    # Store the username, key, and encrypted password in the file
    with open(username + "_passwords.txt", "w") as file:
        file.write(f"Main Pass:{user_key.decode('utf-8')}:{encrypted_password}")

    print("User registered successfully!")
    return True

# Add a new password for the signed-in user
def add_password():
    if not GLOBAL_USERNAME:
        print("No user signed in. Please sign in first.")
        return

    newPassName = input("Enter the name of the password: ")
    newPass = getpass.getpass("Enter the password: ")
    re_enter_password = getpass.getpass("Re-enter password: ")
    while newPass != re_enter_password:
        print("Passwords do not match")
        newPass = getpass.getpass("Enter password: ")
        re_enter_password = getpass.getpass("Re-enter password: ")

    user_key = Fernet.generate_key()
    fernet = Fernet(user_key)

    # Encrypt the password
    encrypted_password = encrypt(newPass, fernet)

    # Append the new password entry to the file
    with open(GLOBAL_USERNAME + "_passwords.txt", "a") as file:
        file.write(f"\n{newPassName}:{user_key.decode('utf-8')}:{encrypted_password}")

    print("Password added successfully!")

def retrieve_password(passname):
    global GLOBAL_USERNAME
    
    with open(GLOBAL_USERNAME + "_passwords.txt", "r") as file:
        data = file.readlines()
        for line in data:
            line = line.strip().split(":")
            if line[0] == passname:
                key = line[1].encode('utf-8')
                encrypted_password = line[2]
                fernet = Fernet(key)
                real_password = decrypt(encrypted_password, fernet)
                print(f"Decrypted password for {passname}: {real_password}")
                return

# Main function
def main():
    global GLOBAL_USERNAME
    GLOBAL_USERNAME = ""
    input_command = input("Enter command (register/add/retrieve): ").strip().lower()

    if input_command == "add":
        if sign_in():
            add_password()
    elif input_command == "register":
        sign_up()
    elif input_command == "retrieve":
        if sign_in():
            passname = input("Enter the name of the password: ")
            retrieve_password(passname)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
