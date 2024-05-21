import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit,
    QListWidget, QLCDNumber, QVBoxLayout, QHBoxLayout,
    QWidget, QTabWidget, QCheckBox, QDialog, QMessageBox, QFormLayout
)

class DecisionMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.decision_data = {}
        self.current_decision_key = None
        self.user_data = {}
        self.current_user = None
        self.load_data()
        self.show_login_dialog()

    def init_ui(self):
        self.setWindowTitle("Decision Maker")
        self.setGeometry(100, 100, 511, 423)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add Question Button
        self.qwestion_add = QPushButton("Добавить вопрос")
        self.qwestion_add.clicked.connect(self.show_question_dialog)
        self.layout.addWidget(self.qwestion_add)

        # Tab Widget for Questions
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.switch_question)

        # Add existing questions as tabs
        for question in self.decision_data.get(self.current_user, {}):
            self.add_tab(question)

        self.update_display()

    def add_tab(self, question):
        tab = QWidget()
        tab_layout = QVBoxLayout()

        arg_input = QLineEdit()
        btn_layout = QHBoxLayout()
        args_layout = QHBoxLayout()
        lcd_layout = QHBoxLayout()
        reset_button = QPushButton("Сброс")
        decision_made_checkbox = QCheckBox("Решение принято")

        arg_za = QPushButton("Добавить аргумент 'за'")
        arg_za.setObjectName("arg_za")  # Set object name
        arg_za.clicked.connect(self.add_argument_for)
        btn_layout.addWidget(arg_za)

        arp_prot = QPushButton("Добавить аргумент 'против'")
        arp_prot.setObjectName("arp_prot")  # Set object name
        arp_prot.clicked.connect(self.add_argument_against)
        btn_layout.addWidget(arp_prot)

        args_za = QListWidget()
        args_za.setObjectName("args_za")
        args_layout.addWidget(args_za)

        args_prot = QListWidget()
        args_prot.setObjectName("args_prot")
        args_layout.addWidget(args_prot)

        lcdNumber_za = QLCDNumber()
        lcdNumber_za.setObjectName("lcdNumber_za")
        lcd_layout.addWidget(lcdNumber_za)

        lcdNumber_protiv = QLCDNumber()
        lcdNumber_protiv.setObjectName("lcdNumber_protiv")
        lcd_layout.addWidget(lcdNumber_protiv)

        reset_button.clicked.connect(self.reset_all)
        decision_made_checkbox.stateChanged.connect(self.handle_decision_made)

        tab_layout.addWidget(arg_input)
        tab_layout.addLayout(btn_layout)
        tab_layout.addLayout(args_layout)
        tab_layout.addLayout(lcd_layout)
        tab_layout.addWidget(reset_button)
        tab_layout.addWidget(decision_made_checkbox)

        tab.setLayout(tab_layout)
        self.tab_widget.addTab(tab, question)

    def switch_question(self, index):
        if index >= 0:
            self.current_decision_key = self.tab_widget.tabText(index)
        else:
            self.current_decision_key = None
        self.update_display()

    def show_question_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить новый вопрос")
        layout = QVBoxLayout(dialog)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(lambda: self.set_question(input_field.text(), dialog))
        layout.addWidget(add_button)

        dialog.exec()

    def set_question(self, new_question, dialog):
        if new_question and new_question not in self.decision_data.get(self.current_user, {}):
            if self.current_user not in self.decision_data:
                self.decision_data[self.current_user] = {}
            self.decision_data[self.current_user][new_question] = {"arguments_for": [], "arguments_against": []}
            self.add_tab(new_question)
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            self.current_decision_key = new_question
            self.save_data()
        dialog.accept()

    def add_argument_for(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            arg_input = current_tab.findChild(QLineEdit)
            argument = arg_input.text()
            self.decision_data[self.current_user][self.current_decision_key]["arguments_for"].append(argument)
            self.save_data()
            self.update_tab_display(current_tab)  # Update the current tab's display
            arg_input.clear()

    def add_argument_against(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            arg_input = current_tab.findChild(QLineEdit)
            argument = arg_input.text()
            self.decision_data[self.current_user][self.current_decision_key]["arguments_against"].append(argument)
            self.save_data()
            self.update_tab_display(current_tab)  # Update the current tab's display
            arg_input.clear()

    def update_display(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            self.update_tab_display(current_tab)  # Update the display for the current tab

    def update_tab_display(self, tab):
        """Updates the display of arguments and counts for a specific tab."""
        args_za = tab.findChild(QListWidget, name="args_za")
        args_prot = tab.findChild(QListWidget, name="args_prot")
        lcdNumber_za = tab.findChild(QLCDNumber, name="lcdNumber_za")
        lcdNumber_protiv = tab.findChild(QLCDNumber, name="lcdNumber_protiv")

        current_data = self.decision_data[self.current_user].get(self.current_decision_key, {"arguments_for": [], "arguments_against": []})
        args_za.clear()
        args_prot.clear()
        for argument in current_data["arguments_for"]:
            args_za.addItem(argument)
        for argument in current_data["arguments_against"]:
            args_prot.addItem(argument)
        lcdNumber_za.display(len(current_data["arguments_for"]))
        lcdNumber_protiv.display(len(current_data["arguments_against"]))

        decision_made_checkbox = tab.findChild(QCheckBox)
        decision_made_checkbox.setEnabled(True)

    def update_lcd_counts(self):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_user][self.current_decision_key]
            self.lcdNumber_za.display(len(current_data["arguments_for"]))
            self.lcdNumber_protiv.display(len(current_data["arguments_against"]))
        else:
            self.lcdNumber_za.display(0)
            self.lcdNumber_protiv.display(0)

    def handle_decision_made(self, state):
        current_tab = self.tab_widget.currentWidget()
        arg_input = current_tab.findChild(QLineEdit)
        arg_za = current_tab.findChild(QPushButton, name="arg_za")  # Find using object name
        arp_prot = current_tab.findChild(QPushButton, name="arp_prot")  # Find using object name
        reset_button = current_tab.findChild(QPushButton)

        if state:
            arg_input.setEnabled(False)
            if arg_za is not None:
                arg_za.setEnabled(False)
            if arp_prot is not None:
                arp_prot.setEnabled(False)
            if reset_button is not None:
                reset_button.setEnabled(False)
        else:
            arg_input.setEnabled(True)
            if arg_za is not None:
                arg_za.setEnabled(True)
            if arp_prot is not None:
                arp_prot.setEnabled(True)
            if reset_button is not None:
                reset_button.setEnabled(True)

    def reset_all(self):
        if self.current_decision_key:
            reply = QMessageBox.question(self, 'Подтвердите сброс', 'Вы уверены, что хотите сбросить текущий вопрос?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                current_index = self.tab_widget.currentIndex()
                self.tab_widget.removeTab(current_index)
                if self.current_user in self.decision_data and self.current_decision_key in self.decision_data[self.current_user]:
                    del self.decision_data[self.current_user][self.current_decision_key]

                # Update current_decision_key BEFORE calling update_display
                if self.tab_widget.count() > 0:
                    self.current_decision_key = self.tab_widget.tabText(self.tab_widget.currentIndex())
                else:
                    self.current_decision_key = None

                self.update_display()
                self.save_data()

    def load_data(self):
        try:
            with open("Сохранение_4_минипроекта.json", "r") as file:
                data = json.load(file)
                self.decision_data = data.get("decisions", {})
                self.user_data = data.get("users", {})
        except FileNotFoundError:
            print("Файл данных не найден.")
            pass

    def save_data(self):
        with open("Сохранение_4_минипроекта.json", "w") as file:
            json.dump({"decisions": self.decision_data, "users": self.user_data}, file)

    def show_login_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Авторизация")

        layout = QFormLayout(dialog)

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Имя пользователя:", username_input)
        layout.addRow("Пароль:", password_input)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(lambda: self.handle_login(username_input.text(), password_input.text(), dialog))
        layout.addWidget(login_button)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(lambda: self.handle_register(username_input.text(), password_input.text(), dialog))
        layout.addWidget(register_button)

        dialog.exec()

    def handle_login(self, username, password, dialog):
        if username in self.user_data and self.user_data[username] == password:
            self.current_user = username
            self.init_ui()  # Reinitialize the UI with the correct user data
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверное имя пользователя или пароль.")

    def handle_register(self, username, password, dialog):
        if username not in self.user_data:
            self.user_data[username] = password
            self.save_data()
            QMessageBox.information(self, "Регистрация успешна", "Теперь вы можете войти в систему.")
        else:
            QMessageBox.warning(self, "Ошибка регистрации", "Пользователь с таким именем уже существует.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
