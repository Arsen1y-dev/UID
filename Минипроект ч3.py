import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QListWidget, QComboBox, QLCDNumber
from PyQt6 import uic

class DecisionMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Минипроект_3.ui', self)

        self.decision_data = {}
        self.current_decision_key = None

        self.load_data()
        self.init_ui()

    def init_ui(self):
        self.qwestion_add = self.findChild(QPushButton, 'qwestion_add')
        self.qwestion_add.clicked.connect(self.set_question)

        self.qwestion_input = self.findChild(QLineEdit, 'qwestion_input')

        self.arg_za = self.findChild(QPushButton, 'arg_za')
        self.arg_za.clicked.connect(self.add_argument_for)

        self.arp_prot = self.findChild(QPushButton, 'arp_prot')
        self.arp_prot.clicked.connect(self.add_argument_against)

        self.args_za = self.findChild(QListWidget, 'args_za')
        self.args_prot = self.findChild(QListWidget, 'args_prot')

        self.lcdNumber_za = self.findChild(QLCDNumber, 'lcdNumber_za')
        self.lcdNumber_protiv = self.findChild(QLCDNumber, 'lcdNumber_protiv')

        self.arg_input = self.findChild(QLineEdit, 'arg_input')
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.reset = self.findChild(QPushButton, 'reset')
        self.reset.clicked.connect(self.reset_all)

        self.comboBox.currentIndexChanged.connect(self.switch_question)

        self.update_display()

    def switch_question(self):
        self.current_decision_key = self.comboBox.currentText()
        self.update_display()

    def set_question(self):
        new_question = self.qwestion_input.text()
        if new_question and new_question not in self.decision_data:
            self.decision_data[new_question] = {"arguments_for": [], "arguments_against": []}
            self.comboBox.addItem(new_question)
            self.comboBox.setCurrentText(new_question)
            self.current_decision_key = new_question
            self.save_data()
        self.qwestion_input.clear()

    def add_argument_for(self):
        if self.current_decision_key:
            argument = self.arg_input.text()
            self.decision_data[self.current_decision_key]["arguments_for"].append(argument)
            self.save_data()
            self.update_display()
        self.arg_input.clear()

    def add_argument_against(self):
        if self.current_decision_key:
            argument = self.arg_input.text()
            self.decision_data[self.current_decision_key]["arguments_against"].append(argument)
            self.save_data()
            self.update_display()
        self.arg_input.clear()

    def update_display(self):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_decision_key]
            self.args_za.clear()
            self.args_prot.clear()
            for argument in current_data["arguments_for"]:
                self.args_za.addItem(argument)
            for argument in current_data["arguments_against"]:
                self.args_prot.addItem(argument)
            self.update_lcd_counts()

    def update_lcd_counts(self):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_decision_key]
            self.lcdNumber_za.display(len(current_data["arguments_for"]))
            self.lcdNumber_protiv.display(len(current_data["arguments_against"]))

    def reset_all(self):
        if self.current_decision_key:
            del self.decision_data[self.current_decision_key]
            self.comboBox.removeItem(self.comboBox.currentIndex())
            self.current_decision_key = None
            self.update_display()
            self.save_data()

    def load_data(self):
        try:
            with open("/Users/arseniy/Documents/GitHub/UID/JSONки/Сохранение 3 минипроекта.json", "r") as file:
                self.decision_data = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("/Users/arseniy/Documents/GitHub/UID/JSONки/Сохранение 3 минипроекта.json", "w") as file:
            json.dump(self.decision_data, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())