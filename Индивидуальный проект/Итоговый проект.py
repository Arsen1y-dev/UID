import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QMainWindow,
    QMenuBar,
    QMenu,
    QComboBox,
    QInputDialog,
    QListWidget,
    QHBoxLayout,
    QSpinBox, # Добавлен QSpinBox для количества
)
from PyQt6.QtGui import (
    QPixmap,
    QAction,  
)
from PyQt6.QtCore import Qt, QSize
import re
import hashlib
import json
from datetime import datetime

# Создаем файлы, если они не существуют
def create_file_if_not_exists(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

create_file_if_not_exists("users.json")
create_file_if_not_exists("services.json")
create_file_if_not_exists("orders.json")


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
        self.setGeometry(100, 100, 400, 350)

        # Создаем файл users.json, если он не существует
        file_path = os.path.join(os.path.dirname(__file__), "users.json")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)

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

        self.label_role = QLabel("Тип пользователя:", self)
        self.combobox_role = QComboBox(self)
        self.combobox_role.addItems(["client", "employee"])

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
        layout.addWidget(self.label_role)
        layout.addWidget(self.combobox_role)
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
        file_path = os.path.join(os.path.dirname(__file__), "users.json")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)
    
        try:
            with open(file_path, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

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
        role = self.combobox_role.currentText()

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
            "phone": phone,
            "role": role 
        }

        with open("users.json", "r") as file:
            users = json.load(file)

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

        file_path = os.path.join(os.path.dirname(__file__), "users.json")

        if not os.path.exists(file_path):
            QMessageBox.critical(self, "Ошибка", "Пользователь с таким логином не найден.")
            return

        with open(file_path, "r") as file:
            users = json.load(file)
            for user_data in users:
                if user_data["login"] == login:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if user_data["password"] == hashed_password:
                        self.user_role = user_data.get("role", "client")
                        self.open_main_window()
                        return

        QMessageBox.critical(self, "Ошибка", "Неправильный логин или пароль.")

    def open_main_window(self):
        self.main_window = MainWindow(self.user_role, self.entry_login.text()) 
        self.main_window.show()
        self.hide()

    def back_to_start(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, user_role, login): 
        super().__init__()
        self.setWindowTitle("Фотоцентр - Главная")
        self.setGeometry(100, 100, 800, 600)
        self.user_role = user_role 
        self.user_login = login  

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        if self.user_role == "employee":
            employee_menu = menubar.addMenu("Сотрудник")
            manage_orders_action = QAction("Управление заказами", self)
            # manage_orders_action.triggered.connect(self.open_manage_orders)
            employee_menu.addAction(manage_orders_action)

            reports_action = QAction("Финансовые отчеты", self)
            # reports_action.triggered.connect(self.open_reports)
            employee_menu.addAction(reports_action)
        else:  # Клиент
            self.services_window = ServicesWindow()
            self.setCentralWidget(self.services_window)

            client_menu = menubar.addMenu("Клиент")
            view_services_action = QAction("Просмотр услуг", self)
            view_services_action.triggered.connect(self.open_services_window)
            client_menu.addAction(view_services_action)

            order_history_action = QAction("История заказов", self)
            order_history_action.triggered.connect(self.open_order_history_window)
            client_menu.addAction(order_history_action)

    def open_services_window(self):
        self.services_window = ServicesWindow()
        self.services_window.show()

    def open_order_history_window(self):
        self.order_history_window = OrderHistoryWindow(self.user_login)  # Передаем login
        self.order_history_window.show()

class ServicesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Услуги")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.services_label = QLabel(self)
        layout.addWidget(self.services_label)
        self.setLayout(layout)

        self.load_services()

    def load_services(self):
        try:
            with open("services.json", "r") as file:
                services = json.load(file)

            services_text = ""
            for service in services:
                services_text += f"ID: {service['id']}, {service['name']} - {service['description']} - {service['price']} руб.\n"
            self.services_label.setText(services_text)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")

class OrderHistoryWindow(QWidget):
    def __init__(self, user_login):  # Принимаем login
        super().__init__()
        self.setWindowTitle("История заказов")
        self.setGeometry(100, 100, 600, 400)
        self.user_login = user_login

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.order_list = QListWidget(self)
        layout.addWidget(self.order_list)
        self.setLayout(layout)

        self.load_order_history()

    def load_order_history(self):
        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)

            for order in orders:
                if order["client_login"] == self.user_login:
                    order_info = f"Заказ №{order['id']} от {order['date']} - Статус: {order['status']} - {order['total_price']} руб."
                    self.order_list.addItem(order_info)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл orders.json не найден.")

class OrderWindow(QWidget):
    def __init__(self, user_login):
        super().__init__()
        self.setWindowTitle("Оформление заказа")
        self.setGeometry(100, 100, 600, 400)
        self.user_login = user_login

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выбор услуги
        self.services_label = QLabel("Выберите услугу:", self)
        layout.addWidget(self.services_label)

        self.services_combobox = QComboBox(self)
        self.load_services()
        layout.addWidget(self.services_combobox)

        # Параметры заказа
        self.parameters_label = QLabel("Параметры заказа:", self)
        layout.addWidget(self.parameters_label)

        # Количество
        self.quantity_label = QLabel("Количество:", self)
        layout.addWidget(self.quantity_label)
        self.quantity_spinbox = QSpinBox(self)
        self.quantity_spinbox.setMinimum(1)
        layout.addWidget(self.quantity_spinbox)

        # TODO: Добавьте другие виджеты для параметров заказа, если необходимо

        # Кнопка "Оформить заказ"
        self.order_button = QPushButton("Оформить заказ", self)
        self.order_button.clicked.connect(self.create_order)
        layout.addWidget(self.order_button)

        self.setLayout(layout)

    def load_services(self):
        file_path = os.path.join(os.path.dirname(__file__), "services.json")
        try:
            with open(file_path, "r") as file:
                services = json.load(file)
                for service in services:
                    self.services_combobox.addItem(f"{service['name']} ({service['price']} руб.)", service['id'])
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")

    def create_order(self):
        selected_service_id = self.services_combobox.currentData()
        quantity = self.quantity_spinbox.value()

        # TODO: Получите другие параметры заказа, если необходимо

        # Находим выбранную услугу
        service = next((s for s in self.services if s["id"] == selected_service_id), None)
        if service:
            total_price = service["price"] * quantity
        else:
            QMessageBox.critical(self, "Ошибка", "Услуга не найдена.")
            return

        # Создаем новый заказ
        new_order = {
            "id": self.get_next_order_id(),
            "client_login": self.user_login,
            "date": datetime.now().strftime("%Y-%m-%d"),  # Текущая дата
            "status": "Новый",
            "services": [
                {
                    "service_id": selected_service_id,
                    "quantity": quantity
                }
                # TODO: Добавьте другие услуги, если выбрано несколько
            ],
            "total_price": total_price
        }

        # Сохраняем заказ в orders.json
        with open("orders.json", "r+") as file:
            orders = json.load(file)
            orders.append(new_order)
            file.seek(0)
            json.dump(orders, file, indent=4)

        QMessageBox.information(self, "Успех", "Заказ успешно оформлен!")

    def get_next_order_id(self):
        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)
                return max(order["id"] for order in orders) + 1 if orders else 1
        except FileNotFoundError:
            return 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec())