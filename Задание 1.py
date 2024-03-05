import re
import hashlib

def check_login(login):
    if re.match("^[a-zA-Z0-9]{5,}$", login):
        return True
    else:
        return False

def check_password(password):
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password)

def check_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

def check_phone(phone):
    return re.match(r'^(\+7|8)[\d ]{10}$', phone)

def user_exists(login, email):
    with open("users.txt", "r") as file:
        for line in file:
            user_data = eval(line) 
            if user_data["login"] == login or user_data["email"] == email:
                return True
    return False

def register_user():
    login = input("Введите свой логин:")
    while not check_login(login):
        print("Неверный логин. Логин должен состоять как минимум из 5 буквенно-цифровых символов.")
        login = input("Введите свой логин:")
    
    email = input("Введите вашу электронную почту:")
    while not check_email(email):
        print("Неправильный адрес электронной почты. Адрес электронной почты должен содержать ровно один символ @ и не может начинаться или заканчиваться им.")
        email = input("Введите вашу электронную почту:")
    
    if user_exists(login, email):
        print("Пользователь с таким логином или адресом электронной почты уже существует. Пожалуйста, выберите другие учетные данные.")
        return
    
    password = input("Введите свой пароль:")
    while not check_password(password):
        print("Неправильный пароль. Пароль должен быть не менее 8 символов длиной, содержать хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ.")
        password = input("Введите свой пароль:")
    
    confirm_password = input("Подтвердите ваш пароль:")
    while password != confirm_password:
        print("Пароли не совпадают. Пожалуйста, попробуйте еще раз.")
        password = input("Введите свой пароль:")
        confirm_password = input("Подтвердите ваш пароль:")
    
    phone = input("Введите ваш номер телефона:")
    while not check_phone(phone):
        print("Неправильный номер телефона. Номер телефона должен быть в формате +7 или 8, за которым следуют 10 цифр с возможными пробелами.")
        phone = input("Введите ваш номер телефона:")
    
    fio = input("Введите ваше полное имя (необязательно):")
    city = input("Введите ваш город (необязательно):")
    about = input("Расскажите о себе (необязательно):")
    
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
    
    print("Пользователь успешно зарегистрирован.")

register_user()
