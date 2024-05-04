import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import re
import hashlib
import json
import os

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добро пожаловать!")
        self.setGeometry(100, 100, 300, 150)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        register_button = QPushButton("Зарегистрироваться", self)
        register_button.clicked.connect(self.open_registration_window)

        login_button = QPushButton("Войти", self)
        login_button.clicked.connect(self.open_login_window)

        layout.addWidget(register_button)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.hide()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_login = QLabel("Логин:", self)
        self.entry_login = QLineEdit(self)

        self.label_email = QLabel("Email:", self)
        self.entry_email = QLineEdit(self)

        self.label_password = QLabel("Пароль:", self)
        self.entry_password = QLineEdit(self)
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.label_confirm_password = QLabel("Подтвердите пароль:", self)
        self.entry_confirm_password = QLineEdit(self)
        self.entry_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.label_phone = QLabel("Телефон:", self)
        self.entry_phone = QLineEdit(self)

        self.button_register = QPushButton("Зарегистрироваться", self)
        self.button_register.clicked.connect(self.register_user)

        self.button_back = QPushButton("Назад", self)
        self.button_back.clicked.connect(self.back_to_start)

        layout.addWidget(self.label_login)
        layout.addWidget(self.entry_login)
        layout.addWidget(self.label_email)
        layout.addWidget(self.entry_email)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.label_confirm_password)
        layout.addWidget(self.entry_confirm_password)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.entry_phone)
        layout.addWidget(self.button_register)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

    def check_login(self, login):
        if not re.match("^[a-zA-Z0-9]{5,}$", login):
            QMessageBox.critical(self, "Ошибка", "Неверный логин. Логин должен состоять как минимум из 5 буквенно-цифровых символов.")
            return False
        return True

    def check_password(self, password):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
            QMessageBox.critical(self, "Ошибка", "Неверный пароль. Пароль должен быть не менее 8 символов длиной, содержать хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ.")
            return False
        return True

    def check_email(self, email):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            QMessageBox.critical(self, "Ошибка", "Неправильный адрес электронной почты. Адрес электронной почты должен содержать ровно один символ @ и не может начинаться или заканчиваться им.")
            return False
        return True

    def check_phone(self, phone):
        if not re.match(r'^(\+7|8)[\d ]{10}$', phone):
            QMessageBox.critical(self, "Ошибка", "Неправильный номер телефона. Номер телефона должен быть в формате +7 или 8, за которым следуют 10 цифр с возможными пробелами.")
            return False
        return True

    def user_exists(self, login, email):
        if not os.path.exists("users.json"):
            return False

        with open("users.json", "r") as file:
            users = json.load(file)
            for user_data in users:
                if user_data["login"] == login or user_data["email"] == email:
                    return True
        return False

    def register_user(self):
        login = self.entry_login.text()
        email = self.entry_email.text()
        password = self.entry_password.text()
        confirm_password = self.entry_confirm_password.text()
        phone = self.entry_phone.text()

        if not (self.check_login(login) and self.check_email(email) and self.check_password(password) and password == confirm_password and self.check_phone(phone)):
            return

        if self.user_exists(login, email):
            QMessageBox.critical(self, "Ошибка", "Пользователь с таким логином или адресом электронной почты уже существует.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user_data = {
            "login": login,
            "password": hashed_password,
            "email": email,
            "phone": phone
        }

        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                users = json.load(file)
        else:
            users = []

        users.append(user_data)

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

        QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован.")
        self.open_new_window()

    def open_new_window(self):
        self.new_window = QWidget()
        self.new_window.setWindowTitle("Успешная регистрация")
        self.new_window.setGeometry(200, 200, 300, 150)
        self.new_window.show()

    def back_to_start(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_login = QLabel("Логин:", self)
        self.entry_login = QLineEdit(self)

        self.label_password = QLabel("Пароль:", self)
        self.entry_password = QLineEdit(self)
        self.entry_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button_login = QPushButton("Войти", self)
        self.button_login.clicked.connect(self.login_user)

        self.button_back = QPushButton("Назад", self)
        self.button_back.clicked.connect(self.back_to_start)

        layout.addWidget(self.label_login)
        layout.addWidget(self.entry_login)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

    def login_user(self):
        login = self.entry_login.text()
        password = self.entry_password.text()

        if not os.path.exists("users.json"):
            QMessageBox.critical(self, "Ошибка", "Пользователь с таким логином не найден.")
            return

        with open("users.json", "r") as file:
            users = json.load(file)
            for user_data in users:
                if user_data["login"] == login:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if user_data["password"] == hashed_password:
                        self.open_new_window()
                        return

        QMessageBox.critical(self, "Ошибка", "Неправильный логин или пароль.")

    def open_new_window(self):
        self.new_window = QWidget()
        self.new_window.setWindowTitle("Успешный вход")
        self.new_window.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Добавляем QLabel для отображения фотографии
        image_label = QLabel(self.new_window)
        pixmap = QPixmap("/Users/arseniy/Documents/GitHub/UID/Задание 6. Регистрация в окне/868FDA56-14D5-4816-97B5-D1E0D88B0E42_1_105_c.jpeg").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Добавляем кнопку для выхода
        logout_button = QPushButton("Выход", self.new_window)
        logout_button.clicked.connect(self.close_windows)

        layout.addWidget(image_label)
        layout.addWidget(logout_button)

        self.new_window.setLayout(layout)

        self.new_window.show()
        self.hide()

    def close_windows(self):
        self.new_window.close()
        self.close()

    def back_to_start(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec())
