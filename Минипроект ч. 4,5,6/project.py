import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QLCDNumber, QCheckBox, QInputDialog, QMessageBox, QMenu,
    QMenuBar, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QAction
import hashlib


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        self.label = QLabel("Welcome to Our App!", self)
        layout.addWidget(self.label)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(self.register_button)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.open_login_window)
        layout.addWidget(self.login_button)

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
        self.setWindowTitle("Registration")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.label = QLabel("Registration Form", self)
        layout.addWidget(self.label)

        self.username_label = QLabel("Username:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.email_label = QLabel("Email:", self)
        layout.addWidget(self.email_label)
        self.email_edit = QLineEdit(self)
        layout.addWidget(self.email_edit)

        self.phone_label = QLabel("Phone:", self)
        layout.addWidget(self.phone_label)
        self.phone_edit = QLineEdit(self)
        layout.addWidget(self.phone_edit)

        self.password_label = QLabel("Password:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.confirm_password_label = QLabel("Confirm Password:", self)
        layout.addWidget(self.confirm_password_label)
        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_edit)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_to_welcome)
        layout.addWidget(self.back_button)

    def register_user(self):
        username = self.username_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not (username and email and phone and password and confirm_password):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            self.password_edit.clear()
            self.confirm_password_edit.clear()
            return
        print(12)
        try:
            with open("users.json", "r", encoding='utf-8') as file:
                for line in file:
                    user_data = json.loads(line)
                    if user_data["username"] == username:
                        QMessageBox.warning(self, "Error", "Username already exists!")
                        return
        except FileNotFoundError:
            pass


        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user_data = {
            "username": username,
            "email": email,
            "phone": phone,
            "password": hashed_password
        }
        print(0)
        with open("users.json", "a", encoding='utf-8') as file:
            json.dump(user_data, file)
            file.write('\n')
        print(1)
        QMessageBox.information(self, "Success", "Registration successful!")
        self.hide()
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()

    def back_to_welcome(self):
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()
        self.hide()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 200)

        layout = QVBoxLayout(self)

        self.label = QLabel("Login Form", self)
        layout.addWidget(self.label)

        self.username_label = QLabel("Username:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.password_label = QLabel("Password:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_to_welcome)
        layout.addWidget(self.back_button)

    def login_user(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not (username and password):
            QMessageBox.warning(self, "Error", "Please enter both username and password!")
            return

        with open("users.json", "r", encoding='utf-8') as file:
            for line in file:
                user_data = json.loads(line)
                if user_data["username"] == username:
                    # Хэширование введенного пароля и сравнение с хэшем в файле
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if user_data["password"] == hashed_password:
                        QMessageBox.information(self, "Success", "Login successful!")
                        app = QApplication.instance()
                        app.user_id = username
                        self.hide()
                        self.DecisionMaker = DecisionMaker()
                        self.DecisionMaker.show()
                        return

        QMessageBox.warning(self, "Error", "Invalid username or password!")
        self.password_edit.clear()

    def back_to_welcome(self):
        self.hide()
        self.WelcomeWindow = WelcomeWindow()
        self.WelcomeWindow.show()


class DecisionMaker(QWidget):
    def __init__(self):
        super().__init__()

        self.decision_data = {}
        self.current_decision_key = None
        self.decision_accepted = {}
        self.decision_checkboxes = {}

        self.tab_widget = QTabWidget()
        self.init_ui()
        self.load_data()
        self.create_shortcuts()

    def init_ui(self):
        self.setWindowTitle("Decision Maker")

        # Create main menu
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")

        add_question_action = QAction("Добавить вопрос", self)
        add_question_action.triggered.connect(self.add_tab)
        file_menu.addAction(add_question_action)

        reset_action = QAction("Сбросить", self)
        reset_action.triggered.connect(self.reset_all)
        file_menu.addAction(reset_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_action = QAction("Справка", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        v_layout = QVBoxLayout()
        v_layout.setMenuBar(self.menu_bar)

        self.tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tab_widget.customContextMenuRequested.connect(self.show_tab_context_menu)

        self.add_tab_button = QPushButton("Добавить вопрос")
        self.add_tab_button.clicked.connect(self.add_tab)

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Введите новый вопрос")

        self.for_count_lcd = QLCDNumber()
        self.against_count_lcd = QLCDNumber()
        self.update_lcd_counts()

        self.arg_input_button = QLineEdit()
        self.arg_input_button.setPlaceholderText("Введите аргумент")

        self.for_button = QPushButton("Добавить аргумент За")
        self.for_button.clicked.connect(self.add_argument_for)

        self.against_button = QPushButton("Добавить аргумент Против")
        self.against_button.clicked.connect(self.add_argument_against)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.reset_all)

        self.arguments_for_list = QListWidget()
        self.arguments_for_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.arguments_for_list.setAcceptDrops(True)
        self.arguments_for_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.arguments_for_list.setDragEnabled(True)
        self.arguments_for_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.arguments_for_list.customContextMenuRequested.connect(
            lambda pos: self.show_argument_context_menu(pos, self.arguments_for_list)
        )

        self.arguments_against_list = QListWidget()
        self.arguments_against_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.arguments_against_list.setAcceptDrops(True)
        self.arguments_against_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.arguments_against_list.setDragEnabled(True)
        self.arguments_against_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.arguments_against_list.customContextMenuRequested.connect(
            lambda pos: self.show_argument_context_menu(pos, self.arguments_against_list)
        )

        self.update_display()

        v_layout.addWidget(self.tab_widget)
        v_layout.addWidget(self.add_tab_button)
        v_layout.addWidget(self.question_input)

        des_layout = QHBoxLayout()
        des_layout.addWidget(QLabel("Количество за: "))
        des_layout.addWidget(QLabel("Количество против: "))
        v_layout.addLayout(des_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.arguments_for_list)
        h_layout.addWidget(self.arguments_against_list)
        v_layout.addLayout(h_layout)

        hx_layout = QHBoxLayout()
        hx_layout.addWidget(self.for_count_lcd)
        hx_layout.addWidget(self.against_count_lcd)
        v_layout.addLayout(hx_layout)

        v_layout.addWidget(self.arg_input_button)
        v_layout.addWidget(self.for_button)
        v_layout.addWidget(self.against_button)
        v_layout.addWidget(self.reset_button)

        self.setLayout(v_layout)

        self.populate_tabs()
        self.tab_widget.currentChanged.connect(self.switch_question)

    def populate_tabs(self):
        for question in self.decision_data.keys():
            self.add_tab(question)

    def add_tab(self, question=None):
        try:
            if not question:
                question, ok = QInputDialog.getText(self, "Добавить вопрос", "Введите новый вопрос:")
                if not ok or question.strip() == "":
                    question = f"Вопрос {self.tab_widget.count() + 1}"
            self.decision_data[question] = {"arguments_for": [], "arguments_against": []}
            self.decision_accepted[question] = False
            tab_index = self.tab_widget.addTab(QWidget(), question)
            tab_layout = QVBoxLayout()
            decision_accepted_checkbox = QCheckBox("Решение принято")
            decision_accepted_checkbox.setChecked(self.decision_accepted[question])
            decision_accepted_checkbox.stateChanged.connect(
                lambda state, q=question: self.toggle_decision_accepted(q, state)
            )
            tab_layout.addWidget(decision_accepted_checkbox)
            self.decision_checkboxes[question] = decision_accepted_checkbox
            self.tab_widget.widget(tab_index).setLayout(tab_layout)
            self.tab_widget.setCurrentIndex(tab_index)
            self.tab_widget.setTabText(tab_index, question)
            self.tab_widget.currentChanged.connect(self.switch_question)
            self.current_decision_key = question
            self.save_data()
            self.update_display()
        except Exception as e:
            print("An exception occurred:", e)

    def remove_tab(self, index):
        try:
            tab_text = self.tab_widget.tabText(index)
            del self.decision_data[tab_text]
            del self.decision_accepted[tab_text]
            del self.decision_checkboxes[tab_text]
            self.tab_widget.removeTab(index)
            self.current_decision_key = None
            self.save_data()
            self.update_display()
        except Exception as e:
            print("An exception occurred:", e)

    def toggle_decision_accepted(self, question, state):
        try:
            self.decision_accepted[question] = state == Qt.CheckState.Checked
            self.save_data()
            self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def toggle_buttons_enabled(self):
        try:
            enabled = self.decision_accepted[self.current_decision_key]
            self.for_button.setDisabled(enabled)
            self.against_button.setDisabled(enabled)
            self.arg_input_button.setDisabled(enabled)
        except Exception as e:
            print("An exception occurred:", e)

    def load_data(self):
        try:
            with open("users_data.json", "r", encoding='utf-8') as file:
                user_data = json.load(file)
                app = QApplication.instance()
                current_user = app.user_id
                if current_user in user_data:
                    data = user_data[current_user]
                    self.decision_data = data["decision_data"]
                    self.decision_accepted = data["decision_accepted"]
                    for question, arguments in self.decision_data.items():
                        tab = QWidget()
                        tab.setObjectName(question)
                        self.tab_widget.addTab(tab, question)
                        decision_accepted_checkbox = QCheckBox("Решение принято")
                        decision_accepted_checkbox.setChecked(self.decision_accepted[question])
                        decision_accepted_checkbox.stateChanged.connect(
                            lambda state, q=question: self.toggle_decision_accepted(q, state))
                        self.decision_checkboxes[question] = decision_accepted_checkbox
                        tab_layout = QVBoxLayout()
                        tab_layout.addWidget(decision_accepted_checkbox)
                        tab.setLayout(tab_layout)
                    self.switch_question(self.tab_widget.currentIndex())
        except Exception as e:
            print("An exception occurred:", e)
            self.decision_data = {}
            self.decision_accepted = {}

    def save_data(self):
        try:
            with open("users_data.json", "r", encoding='utf-8') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}
        app = QApplication.instance()
        current_user = app.user_id
        user_data[current_user] = {
            "decision_data": self.decision_data,
            "decision_accepted": self.decision_accepted
        }
        with open("users_data.json", "w", encoding='utf-8') as f:
            json.dump(user_data, f, indent=4)

    def add_argument_for(self):
        try:
            if self.current_decision_key and not self.decision_accepted[self.current_decision_key]:
                argument = self.arg_input_button.text()
                self.decision_data[self.current_decision_key]["arguments_for"].append(argument)
                self.update_display()
                self.save_data()
                self.arg_input_button.clear()
                self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def add_argument_against(self):
        try:
            if self.current_decision_key and not self.decision_accepted[self.current_decision_key]:
                argument = self.arg_input_button.text()
                self.decision_data[self.current_decision_key]["arguments_against"].append(argument)
                self.update_display()
                self.save_data()
                self.arg_input_button.clear()
                self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def move_argument_up(self, list_widget):
        current_row = list_widget.currentRow()
        if current_row > 0:
            current_item = list_widget.takeItem(current_row)
            list_widget.insertItem(current_row - 1, current_item)
            list_widget.setCurrentRow(current_row - 1)
            self.swap_arguments(list_widget, current_row, current_row - 1)

    def move_argument_down(self, list_widget):
        current_row = list_widget.currentRow()
        if current_row < list_widget.count() - 1 and current_row != -1:
            current_item = list_widget.takeItem(current_row)
            list_widget.insertItem(current_row + 1, current_item)
            list_widget.setCurrentRow(current_row + 1)
            self.swap_arguments(list_widget, current_row, current_row + 1)

    def swap_arguments(self, list_widget, index1, index2):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_decision_key]
            if list_widget is self.arguments_for_list:
                current_data["arguments_for"][index1], current_data["arguments_for"][index2] = \
                    current_data["arguments_for"][index2], current_data["arguments_for"][index1]
            elif list_widget is self.arguments_against_list:
                current_data["arguments_against"][index1], current_data["arguments_against"][index2] = \
                    current_data["arguments_against"][index2], current_data["arguments_against"][index1]
            self.save_data()

    def update_display(self):
        try:
            if self.current_decision_key:
                current_data = self.decision_data[self.current_decision_key]
                self.arguments_for_list.clear()
                self.arguments_against_list.clear()
                for argument in current_data["arguments_for"]:
                    self.arguments_for_list.addItem(argument)
                for argument in current_data["arguments_against"]:
                    self.arguments_against_list.addItem(argument)
                self.update_lcd_counts()
                self.toggle_buttons_enabled()
        except Exception as e:
            print("An exception occurred:", e)

    def update_lcd_counts(self):
        try:
            if self.current_decision_key:
                current_data = self.decision_data[self.current_decision_key]
                self.for_count_lcd.display(len(current_data["arguments_for"]))
                self.against_count_lcd.display(len(current_data["arguments_against"]))
        except Exception as e:
            print("An exception occurred:", e)

    def switch_question(self, index):
        try:
            self.current_decision_key = self.tab_widget.tabText(index)
            self.update_display()
        except Exception as e:
            print("An exception occurred:", e)

    def reset_all(self):
        try:
            if self.current_decision_key:
                reply = QMessageBox.question(self, 'Подтверждение сброса',
                                             'Вы уверены, что хотите сбросить данные вопроса?',
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                             QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    del self.decision_data[self.current_decision_key]
                    del self.decision_accepted[self.current_decision_key]
                    del self.decision_checkboxes[self.current_decision_key]
                    self.tab_widget.removeTab(self.tab_widget.currentIndex())
                    self.current_decision_key = None
                    self.update_display()
                    self.save_data()
        except Exception as e:
            print("An exception occurred:", e)

    def create_shortcuts(self):
        QShortcut(QKeySequence('F1'), self).activated.connect(self.show_help)
        QShortcut(QKeySequence('Ctrl+N'), self).activated.connect(self.add_tab)
        QShortcut(QKeySequence('Shift+Del'), self).activated.connect(self.remove_current_tab)
        QShortcut(QKeySequence('Ctrl+Z'), self).activated.connect(self.undo_last_action)
        QShortcut(QKeySequence('Del'), self).activated.connect(self.delete_selected_argument)

    def show_help(self):
        QMessageBox.information(self, "Справка", "Информация о приложении...")

    def remove_current_tab(self):
        index = self.tab_widget.currentIndex()
        if index != -1:
            self.remove_tab(index)

    def undo_last_action(self):
        # Implement undo functionality if needed
        pass

    def delete_selected_argument(self):
        try:
            if self.current_decision_key:
                list_widget = self.arguments_for_list if self.arguments_for_list.hasFocus() else self.arguments_against_list
                current_row = list_widget.currentRow()
                if current_row != -1:
                    reply = QMessageBox.question(self, 'Удалить аргумент',
                                                 'Вы уверены, что хотите удалить выбранный аргумент?',
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                 QMessageBox.StandardButton.No)
                    if reply == QMessageBox.StandardButton.Yes:
                        item = list_widget.takeItem(current_row)
                        argument = item.text()
                        if list_widget is self.arguments_for_list:
                            self.decision_data[self.current_decision_key]["arguments_for"].remove(argument)
                        else:
                            self.decision_data[self.current_decision_key]["arguments_against"].remove(argument)
                        self.save_data()
                        self.update_display()
        except Exception as e:
            print("An exception occurred:", e)

    def show_tab_context_menu(self, pos):
        index = self.tab_widget.tabBar().tabAt(pos)
        if index != -1:
            menu = QMenu(self)
            rename_action = QAction("Переименовать вкладку", self)
            rename_action.triggered.connect(lambda: self.rename_tab(index))
            delete_action = QAction("Удалить вкладку", self)
            delete_action.triggered.connect(lambda: self.remove_tab(index))
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            menu.exec(self.tab_widget.mapToGlobal(pos))

    def rename_tab(self, index):
        old_name = self.tab_widget.tabText(index)
        new_name, ok = QInputDialog.getText(self, "Переименовать вкладку", "Введите новое имя:", text=old_name)
        if ok and new_name.strip() != "":
            self.decision_data[new_name] = self.decision_data.pop(old_name)
            self.decision_accepted[new_name] = self.decision_accepted.pop(old_name)
            self.decision_checkboxes[new_name] = self.decision_checkboxes.pop(old_name)
            self.decision_checkboxes[new_name].setText(new_name)
            self.tab_widget.setTabText(index, new_name)
            self.save_data()

    def show_argument_context_menu(self, pos, list_widget):
        menu = QMenu(self)
        move_to_opposite_action = QAction("Переместить в противоположный список", self)
        move_to_opposite_action.triggered.connect(lambda: self.move_to_opposite_list(list_widget))
        delete_argument_action = QAction("Удалить аргумент", self)
        delete_argument_action.triggered.connect(lambda: self.delete_selected_argument())
        menu.addAction(move_to_opposite_action)
        menu.addAction(delete_argument_action)
        menu.exec(list_widget.mapToGlobal(pos))

    def move_to_opposite_list(self, list_widget):
        if self.current_decision_key:
            current_row = list_widget.currentRow()
            if current_row != -1:
                item = list_widget.takeItem(current_row)
                argument = item.text()
                opposite_list = (
                    self.arguments_against_list
                    if list_widget is self.arguments_for_list
                    else self.arguments_for_list
                )
                if list_widget is self.arguments_for_list:
                    self.decision_data[self.current_decision_key]["arguments_for"].remove(argument)
                    self.decision_data[self.current_decision_key]["arguments_against"].append(argument)
                else:
                    self.decision_data[self.current_decision_key]["arguments_against"].remove(argument)
                    self.decision_data[self.current_decision_key]["arguments_for"].append(argument)
                opposite_list.addItem(argument)
                self.save_data()
                self.update_display()


def main():
    app = QApplication(sys.argv)

    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()