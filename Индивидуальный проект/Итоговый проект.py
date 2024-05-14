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
    QSpinBox,
    QTableWidget,
    QDateEdit,
    QHeaderView,
    QRadioButton,
    QTableWidgetItem
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
        self.combobox_role.addItems(["client", "employee", "admin"])  # Добавлен "admin"

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
            QMessageBox.critical(self, "Ошибка",
                                 "Неверный логин. Логин должен состоять как минимум из 5 буквенно-цифровых символов.")
            return False
        return True

    def check_password(self, password):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
            QMessageBox.critical(self, "Ошибка",
                                 "Неверный пароль. Пароль должен быть не менее 8 символов длиной, содержать хотя бы одну заглавную букву, одну строчную букву, одну цифру и один специальный символ.")
            return False
        return True

    def check_email(self, email):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            QMessageBox.critical(self, "Ошибка",
                                 "Неправильный адрес электронной почты. Адрес электронной почты должен содержать ровно один символ @ и не может начинаться или заканчиваться им.")
            return False
        return True

    def check_phone(self, phone):
        if not re.match(r'^(\+7|8)[\d ]{10}$', phone):
            QMessageBox.critical(self, "Ошибка",
                                 "Неправильный номер телефона. Номер телефона должен быть в формате +7 или 8, за которым следуют 10 цифр с возможными пробелами.")
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

        if role == "admin":  # Проверка кода для регистрации администратора
            access_code = self.get_access_code()
            if access_code != "0000":
                QMessageBox.critical(self, "Ошибка", "Неверный код доступа для регистрации администратора.")
                return
        elif role == "employee":  # Проверка кода для регистрации сотрудника
            access_code = self.get_access_code()
            if access_code != "1234":
                QMessageBox.critical(self, "Ошибка", "Неверный код доступа для регистрации сотрудника.")
                return

        if not (self.check_login(login) and self.check_email(email) and self.check_password(
                password) and password == confirm_password and self.check_phone(phone)):
            return

        if self.user_exists(login, email):
            QMessageBox.critical(self, "Ошибка",
                                 "Пользователь с таким логином или адресом электронной почты уже существует.")
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

    def get_access_code(self):
        code, ok = QInputDialog.getText(self, "Код доступа", "Введите код доступа для регистрации:")
        if ok:
            return code
        else:
            return None

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
        if self.user_role == "employee":
            self.main_window = EmployeeMainWindow(self.entry_login.text())  # Передаем только login
        elif self.user_role == 'admin':
            self.main_window = AdminMainWindow(self.entry_login.text())
        else:  # Клиент
            self.main_window = ClientMainWindow(self.entry_login.text())
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
        exit_action.triggered.connect(self.back_to_start)  # Подключаем к back_to_start
        file_menu.addAction(exit_action)

        if self.user_role == "employee":
            self.employee_main_window = EmployeeMainWindow(self.user_login)  # Создаем EmployeeMainWindow
            self.setCentralWidget(self.employee_main_window)  # Устанавливаем EmployeeMainWindow как центральный виджет

            employee_menu = menubar.addMenu("Сотрудник")
            manage_services_action = QAction("Управление услугами", self)
            manage_services_action.triggered.connect(self.open_manage_services_window)
            employee_menu.addAction(manage_services_action)

            manage_orders_action = QAction("Управление заказами", self)
            manage_orders_action.triggered.connect(self.open_manage_orders_window)
            employee_menu.addAction(manage_orders_action)

            reports_action = QAction("Финансовые отчеты", self)
            reports_action.triggered.connect(self.open_reports_window)
            employee_menu.addAction(reports_action)
        else:  # Клиент
            # self.services_window = ServicesWindow()
            # self.setCentralWidget(self.services_window)

            client_menu = menubar.addMenu("Клиент")
            view_services_action = QAction("Просмотр услуг", self)
            view_services_action.triggered.connect(self.open_services_window)
            client_menu.addAction(view_services_action)

            make_order_action = QAction("Оформить заказ", self)
            make_order_action.triggered.connect(self.open_order_window)
            client_menu.addAction(make_order_action)

            order_history_action = QAction("История заказов", self)
            order_history_action.triggered.connect(self.open_order_history_window)
            client_menu.addAction(order_history_action)

    def open_services_window(self):
        self.services_window = ServicesWindow()
        self.services_window.show()

    def open_order_history_window(self):
        self.order_history_window = OrderHistoryWindow(self.user_login)  # Передаем login
        self.order_history_window.show()

    def open_order_window(self):
        self.order_window = OrderWindow(self.user_login)
        self.order_window.show()

    def open_manage_services_window(self):
        self.manage_services_window = ManageServicesWindow()
        self.manage_services_window.show()

    def open_manage_orders_window(self):
        self.manage_orders_window = ManageOrdersWindow()
        self.manage_orders_window.show()

    def open_reports_window(self):
        self.reports_window = ReportsWindow()
        self.reports_window.show()

    def back_to_start(self):  # Добавляем функцию выхода
        self.close()
        self.start_window = StartWindow()
        self.start_window.show()


class ClientMainWindow(QMainWindow):
    def __init__(self, user_login):
        super().__init__()
        self.setWindowTitle("Фотоцентр - Главная (Клиент)")
        self.setGeometry(100, 100, 600, 400)
        self.user_login = user_login

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Приветствие
        welcome_label = QLabel(f"Добро пожаловать, {self.user_login}!", self)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Логотип
        logo_label = QLabel(self)
        pixmap = QPixmap("logo.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Кнопки действий
        buttons_layout = QHBoxLayout()
        view_services_button = QPushButton("Просмотр услуг", self)
        view_services_button.clicked.connect(self.open_services_window)
        buttons_layout.addWidget(view_services_button)

        make_order_button = QPushButton("Оформить заказ", self)
        make_order_button.clicked.connect(self.open_order_window)
        buttons_layout.addWidget(make_order_button)

        order_history_button = QPushButton("История заказов", self)
        order_history_button.clicked.connect(self.open_order_history_window)
        buttons_layout.addWidget(order_history_button)

        layout.addLayout(buttons_layout)

        # Кнопка "Выйти"
        exit_button = QPushButton("Выйти", self)
        exit_button.clicked.connect(self.back_to_start_window)
        layout.addWidget(exit_button)

    def open_services_window(self):
        self.services_window = ServicesWindow()
        self.services_window.show()

    def open_order_window(self):
        self.order_window = OrderWindow(self.user_login)
        self.order_window.show()

    def open_order_history_window(self):
        self.order_history_window = OrderHistoryWindow(self.user_login)
        self.order_history_window.show()

    def back_to_start_window(self):
        self.close()
        self.start_window = StartWindow()
        self.start_window.show()


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
    def __init__(self, user_login):
        super().__init__()
        self.setWindowTitle("История заказов")
        self.setGeometry(100, 100, 700, 400)
        self.user_login = user_login

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.orders_table = QTableWidget(self)
        self.orders_table.setColumnCount(5)  # Добавляем столбец для деталей заказа
        self.orders_table.setHorizontalHeaderLabels(["ID", "Дата", "Статус", "Стоимость", "Детали"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.orders_table.cellClicked.connect(self.show_order_details)
        layout.addWidget(self.orders_table)

        self.setLayout(layout)

        self.load_order_history()

    def load_order_history(self):
        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)
                # Проверка на пустой список заказов
                if not orders:
                    QMessageBox.information(self, "Информация", "История заказов пуста.")
                    return

                self.orders_table.setRowCount(len(orders))
                for row, order in enumerate(orders):
                    if order["client_login"] == self.user_login:
                        self.orders_table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
                        self.orders_table.setItem(row, 1, QTableWidgetItem(order["date"]))
                        self.orders_table.setItem(row, 2, QTableWidgetItem(order["status"]))
                        self.orders_table.setItem(row, 3, QTableWidgetItem(str(order["total_price"])))
                        self.orders_table.setItem(row, 4, QTableWidgetItem("Показать детали"))
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл orders.json не найден.")

    def show_order_details(self, row, column):
        if column == 4:  # Проверяем, что клик был по столбцу "Детали"
            # Проверяем, что элемент существует
            if self.orders_table.item(row, 0) is not None:
                order_id = int(self.orders_table.item(row, 0).text())
                try:
                    with open("orders.json", "r") as file:
                        orders = json.load(file)
                        order = next((o for o in orders if o["id"] == order_id), None)
                        if order:
                            details = f"Заказ №{order['id']}\n" \
                                      f"Клиент: {order['client_login']}\n" \
                                      f"Дата: {order['date']}\n" \
                                      f"Статус: {order['status']}\n" \
                                      f"Услуги:\n" + \
                                      "\n".join(
                                          [f"   - {s['quantity']}x {self.get_service_name(s['service_id'])}" for s in
                                           order["services"]]) + \
                                      f"\nСтоимость: {order['total_price']} руб."
                            QMessageBox.information(self, "Детали заказа", details)
                except FileNotFoundError:
                    QMessageBox.critical(self, "Ошибка", "Файл orders.json не найден.")

    def get_service_name(self, service_id):
        try:
            with open("services.json", "r") as file:
                services = json.load(file)
                service = next((s for s in services if s["id"] == service_id), None)
                return service["name"] if service else "Неизвестная услуга"
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")
            return "Неизвестная услуга"


class OrderWindow(QWidget):
    def __init__(self, user_login):
        super().__init__()
        self.setWindowTitle("Оформление заказа")
        self.setGeometry(100, 100, 600, 400)
        self.user_login = user_login
        self.selected_services = []  # Список выбранных услуг

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Выбор услуги
        self.services_label = QLabel("Выберите услугу:", self)
        layout.addWidget(self.services_label)

        self.services_list = QListWidget(self)
        self.load_services()
        layout.addWidget(self.services_list)

        # Выбор количества
        self.quantity_label = QLabel("Количество:", self)
        layout.addWidget(self.quantity_label)
        self.quantity_spinbox = QSpinBox(self)
        self.quantity_spinbox.setMinimum(1)
        layout.addWidget(self.quantity_spinbox)

        # Выбор типа бумаги (для печати фотографий)
        self.paper_type_label = QLabel("Тип бумаги:", self)
        layout.addWidget(self.paper_type_label)

        self.glossy_radio = QRadioButton("Глянцевая", self)
        self.matte_radio = QRadioButton("Матовая", self)
        layout.addWidget(self.glossy_radio)
        layout.addWidget(self.matte_radio)

        # Кнопки "Добавить услугу" и "Оформить заказ"
        buttons_layout = QHBoxLayout()
        self.add_service_button = QPushButton("Добавить услугу", self)
        self.add_service_button.clicked.connect(self.add_selected_service)
        buttons_layout.addWidget(self.add_service_button)

        self.order_button = QPushButton("Оформить заказ", self)
        self.order_button.clicked.connect(self.create_order)
        buttons_layout.addWidget(self.order_button)
        layout.addLayout(buttons_layout)

        # Отображение выбранных услуг
        self.selected_services_label = QLabel("Выбранные услуги:", self)
        layout.addWidget(self.selected_services_label)
        self.selected_services_list = QListWidget(self)
        layout.addWidget(self.selected_services_list)

        # Отображение общей стоимости
        self.total_price_label = QLabel("Общая стоимость: 0 руб.", self)
        layout.addWidget(self.total_price_label)

        self.setLayout(layout)

    def load_services(self):
        file_path = os.path.join(os.path.dirname(__file__), "services.json")
        try:
            with open(file_path, "r") as file:
                self.services = json.load(file)
                for service in self.services:
                    self.services_list.addItem(f"{service['name']} ({service['price']} руб.)")
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")

    def add_selected_service(self):
        selected_item = self.services_list.currentItem()
        if selected_item:
            service_name = selected_item.text().split(" (")[0]
            service = next((s for s in self.services if s["name"] == service_name), None)
            if service:
                quantity = self.quantity_spinbox.value()
                paper_type = "Глянцевая" if self.glossy_radio.isChecked() else "Матовая" if self.matte_radio.isChecked() else None

                # TODO: Добавьте обработку других параметров заказа, если необходимо

                self.selected_services.append({
                    "service_id": service["id"],
                    "quantity": quantity,
                    "paper_type": paper_type
                })
                self.selected_services_list.addItem(f"{quantity}x {service_name} ({paper_type})")
                self.update_total_price()

    def update_total_price(self):
        total_price = 0
        for selected_service in self.selected_services:
            service = next((s for s in self.services if s["id"] == selected_service["service_id"]), None)
            if service:
                total_price += service["price"] * selected_service["quantity"]
        self.total_price_label.setText(f"Общая стоимость: {total_price} руб.")

    def create_order(self):
        if not self.selected_services:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одну услугу.")
            return

        new_order = {
            "id": self.get_next_order_id(),
            "client_login": self.user_login,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Новый",
            "services": self.selected_services,
            "total_price": self.get_total_price()
        }

        with open("orders.json", "r+") as file:
            orders = json.load(file)
            orders.append(new_order)
            file.seek(0)
            json.dump(orders, file, indent=4)

        QMessageBox.information(self, "Успех", "Заказ успешно оформлен!")
        self.selected_services = []
        self.selected_services_list.clear()
        self.update_total_price()

    def get_next_order_id(self):
        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)
                if orders:  # Проверка на пустой список
                    return max(order["id"] for order in orders) + 1
                else:
                    return 1
        except FileNotFoundError:
            return 1

    def get_total_price(self):
        total_price = 0
        for selected_service in self.selected_services:
            service = next((s for s in self.services if s["id"] == selected_service["service_id"]), None)
            if service:
                total_price += service["price"] * selected_service["quantity"]
        return total_price


class ManageServicesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление услугами")
        self.setGeometry(100, 100, 500, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.services_table = QTableWidget(self)
        self.services_table.setColumnCount(4)
        self.services_table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Цена"])
        self.services_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.services_table)

        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.add_service)
        buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать", self)
        self.edit_button.clicked.connect(self.edit_service)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить", self)
        self.delete_button.clicked.connect(self.delete_service)
        buttons_layout.addWidget(self.delete_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.load_services()

    def load_services(self):
        try:
            with open("services.json", "r") as file:
                self.services = json.load(file)
                self.update_services_table()
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")

    def update_services_table(self):
        self.services_table.setRowCount(len(self.services))
        for row, service in enumerate(self.services):
            self.services_table.setItem(row, 0, QTableWidgetItem(str(service["id"])))
            self.services_table.setItem(row, 1, QTableWidgetItem(service["name"]))
            self.services_table.setItem(row, 2, QTableWidgetItem(service["description"]))
            self.services_table.setItem(row, 3, QTableWidgetItem(str(service["price"])))

    def add_service(self):
        name, ok = QInputDialog.getText(self, "Добавление услуги", "Название:")
        if ok:
            description, ok = QInputDialog.getText(self, "Добавление услуги", "Описание:")
            if ok:
                try:
                    price, ok = QInputDialog.getDouble(self, "Добавление услуги", "Цена:")
                    if ok:
                        new_id = max([s["id"] for s in self.services]) + 1 if self.services else 1
                        new_service = {"id": new_id, "name": name, "description": description, "price": price}
                        self.services.append(new_service)
                        self.save_services()
                        self.update_services_table()
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Некорректное значение цены.")

    def edit_service(self):
        row = self.services_table.currentRow()
        if row >= 0:
            service_id = int(self.services_table.item(row, 0).text())
            service = next((s for s in self.services if s["id"] == service_id), None)
            if service:
                name, ok = QInputDialog.getText(self, "Редактирование услуги", "Название:", text=service["name"])
                if ok:
                    description, ok = QInputDialog.getText(self, "Редактирование услуги", "Описание:",
                                                           text=service["description"])
                    if ok:
                        try:
                            price, ok = QInputDialog.getDouble(self, "Редактирование услуги", "Цена:",
                                                               value=service["price"])
                            if ok:
                                service["name"] = name
                                service["description"] = description
                                service["price"] = price
                                self.save_services()
                                self.update_services_table()
                        except ValueError:
                            QMessageBox.warning(self, "Ошибка", "Некорректное значение цены.")

    def delete_service(self):
        row = self.services_table.currentRow()
        if row >= 0:
            service_id = int(self.services_table.item(row, 0).text())
            confirm = QMessageBox.question(self, "Подтверждение", f"Удалить услугу с ID {service_id}?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                self.services = [s for s in self.services if s["id"] != service_id]
                self.save_services()
                self.update_services_table()

    def save_services(self):
        try:
            with open("services.json", "w") as file:
                json.dump(self.services, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении услуг: {e}")


class ManageOrdersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление заказами")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.orders_table = QTableWidget(self)
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Клиент", "Дата", "Статус", "Услуги", "Стоимость"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.orders_table.itemSelectionChanged.connect(self.show_order_details)
        layout.addWidget(self.orders_table)

        self.order_details_label = QLabel("Выберите заказ для просмотра деталей", self)
        layout.addWidget(self.order_details_label)

        self.status_combobox = QComboBox(self)
        self.status_combobox.addItems(["Новый", "В обработке", "Готов", "Выдан"])
        self.status_combobox.currentIndexChanged.connect(self.update_order_status)
        layout.addWidget(self.status_combobox)

        self.setLayout(layout)
        self.load_orders()

    def load_orders(self):
        try:
            with open("orders.json", "r") as file:
                self.orders = json.load(file)
                self.update_orders_table()
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл orders.json не найден.")

    def update_orders_table(self):
        self.orders_table.setRowCount(len(self.orders))
        for row, order in enumerate(self.orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
            self.orders_table.setItem(row, 1, QTableWidgetItem(order["client_login"]))
            self.orders_table.setItem(row, 2, QTableWidgetItem(order["date"]))
            self.orders_table.setItem(row, 3, QTableWidgetItem(order["status"]))
            services_text = ", ".join(
                [f"{s['quantity']}x {self.get_service_name(s['service_id'])}" for s in order["services"]])
            self.orders_table.setItem(row, 4, QTableWidgetItem(services_text))
            self.orders_table.setItem(row, 5, QTableWidgetItem(str(order["total_price"])))

    def show_order_details(self):
        row = self.orders_table.currentRow()
        if row >= 0:
            order_id = int(self.orders_table.item(row, 0).text())
            order = next((o for o in self.orders if o["id"] == order_id), None)
            if order:
                details = f"Заказ №{order['id']}\n" \
                          f"Клиент: {order['client_login']}\n" \
                          f"Дата: {order['date']}\n" \
                          f"Статус: {order['status']}\n" \
                          f"Услуги:\n" + \
                          "\n".join([f"   - {s['quantity']}x {self.get_service_name(s['service_id'])}" for s in
                                     order["services"]]) + \
                          f"\nСтоимость: {order['total_price']} руб."
                self.order_details_label.setText(details)
                self.status_combobox.setCurrentText(order["status"])  # Устанавливаем текущий статус в combobox
            else:
                self.order_details_label.setText("Заказ не найден.")
        else:
            self.order_details_label.setText("Выберите заказ для просмотра деталей")

    def get_service_name(self, service_id):
        try:
            with open("services.json", "r") as file:
                services = json.load(file)
                service = next((s for s in services if s["id"] == service_id), None)
                return service["name"] if service else "Неизвестная услуга"
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")
            return "Неизвестная услуга"

    def update_order_status(self):
        row = self.orders_table.currentRow()
        if row >= 0:
            order_id = int(self.orders_table.item(row, 0).text())
            order = next((o for o in self.orders if o["id"] == order_id), None)
            if order:
                new_status = self.status_combobox.currentText()
                order["status"] = new_status
                self.save_orders()
                self.update_orders_table()

    def save_orders(self):
        try:
            with open("orders.json", "w") as file:
                json.dump(self.orders, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении заказов: {e}")


class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Финансовые отчеты")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        date_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setDate(datetime.now())  # Устанавливаем текущую дату
        date_layout.addWidget(QLabel("Начало периода:", self))
        date_layout.addWidget(self.start_date_edit)
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setDate(datetime.now())  # Устанавливаем текущую дату
        date_layout.addWidget(QLabel("Конец периода:", self))
        date_layout.addWidget(self.end_date_edit)
        layout.addLayout(date_layout)

        self.generate_button = QPushButton("Сгенерировать отчет", self)
        self.generate_button.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_button)

        self.report_label = QLabel(self)
        layout.addWidget(self.report_label)

        self.setLayout(layout)

    def generate_report(self):
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()

        try:
            with open("orders.json", "r") as file:
                orders = json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл orders.json не найден.")
            return

        filtered_orders = [order for order in orders if
                           start_date <= datetime.strptime(order["date"], "%Y-%m-%d").date() <= end_date]

        total_sales = sum([order["total_price"] for order in filtered_orders])
        order_count = len(filtered_orders)

        # Расчет популярных услуг
        service_counts = {}
        for order in filtered_orders:
            for service in order["services"]:
                service_id = service["service_id"]
                if service_id in service_counts:
                    service_counts[service_id] += service["quantity"]
                else:
                    service_counts[service_id] = service["quantity"]

        popular_services = sorted(service_counts.items(), key=lambda item: item[1], reverse=True)


        # Добавление информации о популярных услугах в report_text
        report_text = f"Отчет за период с {start_date.strftime('%Y-%m-%d')} по {end_date.strftime('%Y-%m-%d')}\n\n" \
                      f"Общая сумма продаж: {total_sales} руб.\n" \
                      f"Количество заказов: {order_count}\n" \
                      f"\nСамые популярные услуги:\n"
        for service_id, count in popular_services[:3]:  # Выводим топ-3 популярных услуг
            service_name = self.get_service_name(service_id)
            report_text += f" - {service_name}: {count} заказов\n"

        self.report_label.setText(report_text)

    def get_service_name(self, service_id):
        try:
            with open("services.json", "r") as file:
                services = json.load(file)
                service = next((s for s in services if s["id"] == service_id), None)
                return service["name"] if service else "Неизвестная услуга"
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл services.json не найден.")
            return "Неизвестная услуга"


class AdminMainWindow(QMainWindow):  # Окно для администратора
    def __init__(self, user_login):
        super().__init__()
        self.setWindowTitle("Фотоцентр - Главная (Администратор)")
        self.setGeometry(100, 100, 600, 400)
        self.user_login = user_login

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Приветствие
        welcome_label = QLabel(f"Добро пожаловать, {self.user_login}!", self)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Кнопки действий
        buttons_layout = QHBoxLayout()
        users_button = QPushButton("Управление пользователями", self)
        users_button.clicked.connect(self.open_users_window)
        buttons_layout.addWidget(users_button)

        reports_button = QPushButton("Просмотр отчетов", self)
        reports_button.clicked.connect(self.open_reports_window)
        buttons_layout.addWidget(reports_button)

        layout.addLayout(buttons_layout)

        # Кнопка "Выйти"
        exit_button = QPushButton("Выйти", self)
        exit_button.clicked.connect(self.back_to_start_window)
        layout.addWidget(exit_button)

    def open_users_window(self):
        self.users_window = UsersWindow()
        self.users_window.show()

    def open_reports_window(self):
        self.reports_window = ReportsWindow()
        self.reports_window.show()

    def back_to_start_window(self):
        self.close()
        self.start_window = StartWindow()
        self.start_window.show()


class UsersWindow(QWidget):  # Окно управления пользователями
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление пользователями")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.users_table = QTableWidget(self)
        self.users_table.setColumnCount(5)  # 5 столбцов: login, email, phone, role, password(hidden)
        self.users_table.setHorizontalHeaderLabels(["Логин", "Email", "Телефон", "Роль"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.users_table)

        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.add_user)
        buttons_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Редактировать", self)
        self.edit_button.clicked.connect(self.edit_user)
        buttons_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Удалить", self)
        self.delete_button.clicked.connect(self.delete_user)
        buttons_layout.addWidget(self.delete_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                self.users = json.load(file)
                self.update_users_table()
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл users.json не найден.")

    def update_users_table(self):
        self.users_table.setRowCount(len(self.users))
        for row, user in enumerate(self.users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user["login"]))
            self.users_table.setItem(row, 1, QTableWidgetItem(user["email"]))
            self.users_table.setItem(row, 2, QTableWidgetItem(user["phone"]))
            self.users_table.setItem(row, 3, QTableWidgetItem(user["role"]))
            # self.users_table.setItem(row, 4, QTableWidgetItem(user["password"]))  # Пароль не отображаем

    def add_user(self):
        login, ok = QInputDialog.getText(self, "Добавление пользователя", "Логин:")
        if ok:
            email, ok = QInputDialog.getText(self, "Добавление пользователя", "Email:")
            if ok:
                phone, ok = QInputDialog.getText(self, "Добавление пользователя", "Телефон:")
                if ok:
                    role, ok = QInputDialog.getItem(self, "Добавление пользователя", "Роль:",
                                                    ["client", "employee", "admin"], 0, False)
                    if ok:
                        password, ok = QInputDialog.getText(self, "Добавление пользователя", "Пароль:",
                                                            echo=QLineEdit.EchoMode.Password)
                        if ok:
                            hashed_password = hashlib.sha256(password.encode()).hexdigest()
                            new_user = {"login": login, "email": email, "phone": phone, "role": role,
                                        "password": hashed_password}
                            self.users.append(new_user)
                            self.save_users()
                            self.update_users_table()

    def edit_user(self):
        row = self.users_table.currentRow()
        if row >= 0:
            user = self.users[row]
            login, ok = QInputDialog.getText(self, "Редактирование пользователя", "Логин:", text=user["login"])
            if ok:
                email, ok = QInputDialog.getText(self, "Редактирование пользователя", "Email:", text=user["email"])
                if ok:
                    phone, ok = QInputDialog.getText(self, "Редактирование пользователя", "Телефон:",
                                                     text=user["phone"])
                    if ok:
                        role, ok = QInputDialog.getItem(self, "Редактирование пользователя", "Роль:",
                                                        ["client", "employee", "admin"],
                                                        ["client", "employee", "admin"].index(user["role"]), False)
                        if ok:
                            password, ok = QInputDialog.getText(self, "Редактирование пользователя", "Пароль:",
                                                                echo=QLineEdit.EchoMode.Password)
                            if ok:
                                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                                user["login"] = login
                                user["email"] = email
                                user["phone"] = phone
                                user["role"] = role
                                user["password"] = hashed_password
                                self.save_users()
                                self.update_users_table()

    def delete_user(self):
        row = self.users_table.currentRow()
        if row >= 0:
            confirm = QMessageBox.question(self, "Подтверждение",
                                           f"Удалить пользователя {self.users[row]['login']}?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                del self.users[row]
                self.save_users()
                self.update_users_table()

    def save_users(self):
        try:
            with open("users.json", "w") as file:
                json.dump(self.users, file, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении пользователей: {e}")


class EmployeeMainWindow(QMainWindow):  # Окно для сотрудника
    def __init__(self, user_login):
        super().__init__()
        self.setWindowTitle("Фотоцентр - Главная (Сотрудник)")
        self.setGeometry(100, 100, 600, 400)
        self.user_login = user_login

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Приветствие
        welcome_label = QLabel(f"Добро пожаловать, {self.user_login}!", self)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        # Кнопки действий
        buttons_layout = QHBoxLayout()
        manage_orders_button = QPushButton("Управление заказами", self)
        manage_orders_button.clicked.connect(self.open_manage_orders_window)
        buttons_layout.addWidget(manage_orders_button)

        reports_button = QPushButton("Просмотр отчетов", self)
        reports_button.clicked.connect(self.open_reports_window)
        buttons_layout.addWidget(reports_button)

        layout.addLayout(buttons_layout)

        # Кнопка "Выйти"
        exit_button = QPushButton("Выйти", self)
        exit_button.clicked.connect(self.back_to_start_window)
        layout.addWidget(exit_button)

    def open_manage_orders_window(self):
        self.manage_orders_window = ManageOrdersWindow()
        self.manage_orders_window.show()

    def open_reports_window(self):
        self.reports_window = ReportsWindow()
        self.reports_window.show()

    def back_to_start_window(self):
        self.close()
        self.start_window = StartWindow()
        self.start_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec())
