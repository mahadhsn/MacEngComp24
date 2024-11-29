import requests
import getpass

BASE_URL = 'http://127.0.0.1:5000'

def register_user(email, password):
    response = requests.post(f'{BASE_URL}/register', json={'email': email, 'password': password})
   
    return response.status_code

def add_password(email, name, password):
    response = requests.post(f'{BASE_URL}/add_password', json={'email': email, 'name': name, 'password': password})
    print( response.json().get('message'))
    return response.status_code

def get_password(name, email):
    response = requests.get(f'{BASE_URL}/get_password/{email}/{name}')    
    if response.status_code == 200:
        print( "password is ", response.json().get('password'))
        return response.json().get('password')
    else:
        print("Error: ", response.json().get('error'))

def get_passwords(email):
    response = requests.get(f'{BASE_URL}/get_passwords/{email}')
    for password in response.json().get('passwords'):
        print(f"Name: {password.get('name')}, Password: {password.get('decrypted_password')}")
    return response.status_code

def get_all_data():
    response = requests.get(f'{BASE_URL}/get_all_data')
    print( response.json().get('message'))

def sign_in():
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")

    response = requests.post(f'{BASE_URL}/login', json={'email': email, 'password': password})
    if response.status_code == 200:
        print('Login successful')
        return True
    else:
        print('Login failed:', response.json())
        return False

def sign_up():
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")

    response = register_user(email, password)
    if response == 201:
        print('User successfully registered')
    else:
        print('User registration failed')




def main():
    input_command = input("Enter command (register/add/get/getall): ").strip().lower()

    if input_command == "add":
        if sign_in():
            email = input("Enter email: ")
            passname = input("Enter the name of the password: ")
            password = getpass.getpass("Enter the password: ")
            add_password(email, passname, password)
    elif input_command == "register":
        sign_up()
    elif input_command == "get":
        if sign_in():
            email = input("Enter email: ")
            passname = input("Enter the name of the password: ")
            get_password(passname, email)
    elif input_command == "getall":
        if sign_in():
            email = input("Enter email: ")
            get_passwords(email)
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
