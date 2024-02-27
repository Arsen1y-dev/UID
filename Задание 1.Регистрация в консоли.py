import re

def login_(login):
    return re.match(r'^[a-zA-Z0-9]{5,}$', login)

def password_(password):
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password)

def email_(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

def phone_(phone):
    return re.match(r'^(\+7|8)[\d ]{10}$', phone)

def registration():
    login = input("Введите логин: ")
    while not login_(login):
        print("Логин должен состоять не менее чем из 5 символов из набора латинских букв и цифр.")
        login = input("Введите логин: ")

    password = input("Введите пароль: ")
    while not password_(password):
        print("Пароль должен состоять не менее чем из 8 символов, содержать строчные и прописные буквы, цифру и специальный символ.")
        password = input("Введите пароль: ")

    password_repeat = input("Повторите пароль: ")
    while password != password_repeat:
        print("Пароли не совпадают.")
        password = input("Введите пароль: ")
        password_repeat = input("Повторите пароль: ")

    email = input("Введите адрес электронной почты: ")
    while not email_(email):
        print("Некорректный адрес электронной почты.")
        email = input("Введите адрес электронной почты: ")

    phone = input("Введите номер телефона: ")
    while not phone_(phone):
        print("Некорректный номер телефона.")
        phone = input("Введите номер телефона: ")


    full_name = input("Введите ФИО (по желанию): ")
    city = input("Введите город (по желанию): ")
    about = input("Расскажите о себе (по желанию): ")

    with open("users.txt", "a") as file:
        file.write(f"Логин: {login}\nПароль: {password}\nEmail: {email}\nТелефон: {phone}\n")
        file.write(f"ФИО: {full_name}\nГород: {city}\nО себе: {about}\n\n")
    print("Регистрация прошла успешно.")

registration()
