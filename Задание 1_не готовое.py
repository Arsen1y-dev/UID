import re
import hashlib

def check_login(login):
    if re.match("^[a-zA-Z0-9]{5,}$", login):
        return True
    else:
        return False

def check_password(password):
    if len(password) < 8:
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(not char.isalnum() for char in password):
        return False
    return True

def check_email(email):
    if email.count('@') != 1:
        return False
    if email.startswith('@') or email.endswith('@'):
        return False
    return True

def check_phone(phone):
    if re.match("^(8|\+7)[0-9]{10}$", phone.replace(" ", "")):
        return True
    else:
        return False

def register_user():
    login = input("Введите свой логин:")
    while not check_login(login):
        print("Неверный логин. Логин должен состоять как минимум из 5 буквенно-цифровых символов.")
        login = input("Введите свой логин:")
    
    password = input("Введите свой пароль:")
    while not check_password(password):
        print("Invalid password. Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        password = input("Enter your password: ")
    
    confirm_password = input("Confirm your password: ")
    while password != confirm_password:
        print("Passwords do not match. Please try again.")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
    
    email = input("Enter your email: ")
    while not check_email(email):
        print("Invalid email. Email must contain exactly one @ symbol, and cannot start or end with it.")
        email = input("Enter your email: ")
    
    phone = input("Enter your phone number: ")
    while not check_phone(phone):
        print("Invalid phone number. Phone number must be in the format +7 or 8 followed by 10 digits with optional spaces.")
        phone = input("Enter your phone number: ")
    
    fio = input("Enter your full name (optional): ")
    city = input("Enter your city (optional): ")
    about = input("Tell us about yourself (optional): ")
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    user_data = {
        "login": login,
        "password": hashed_password,
        "email": email,
        "phone": phone,
        "full_name": fio,
        "city": city,
        "about": about
    }
    
    with open("users.txt", "a") as file:
        file.write(str(user_data) + "\n")
    
    print("User registered successfully.")

register_user()
