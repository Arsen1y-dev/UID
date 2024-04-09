import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QListWidget
from PyQt6 import uic

class DecisionMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Минипроект 2.ui', self)


        self.arguments_for = []
        self.arguments_against = []
        self.current_question = "Вопрос"

        self.for_count = 0
        self.against_count = 0

        self.load_data()
        self.init_ui()

    def init_ui(self):

        self.set_question_button = self.findChild(QPushButton, 'qwestion_add')
        self.set_question_button.clicked.connect(self.set_question)
        self.question_input = self.findChild(QLineEdit, 'qwestion_input')
        self.question_label = self.findChild(QLabel, 'qwestion')


        self.arg_input_button = self.findChild(QLineEdit, 'arg_input')
        self.for_button = self.findChild(QPushButton, 'arg_za')
        self.against_button = self.findChild(QPushButton, 'arp_prot')

        self.prot = self.findChild(QLabel, 'prot')
        self.za = self.findChild(QLabel, 'za')

        self.arguments_for_list = self.findChild(QListWidget, 'args_za')
        self.arguments_against_list = self.findChild(QListWidget, 'args_prot')

        self.against_count_button = self.findChild(QLabel, 'num_prot')
        self.for_count_button = self.findChild(QLabel, 'num_za')

        self.reset_button = self.findChild(QPushButton, 'reset')

        self.for_button.clicked.connect(self.add_argument_for)

        self.against_button.clicked.connect(self.add_argument_against)

        self.reset_button.clicked.connect(self.reset_all)

        self.update_display()


    def set_question(self):
        self.current_question = self.question_input.text()
        self.question_input.clear()
        self.update_display()
        self.save_data()

    def add_argument_for(self):
        argument = self.arg_input_button.text()
        self.arguments_for.append(argument)
        self.save_data()
        self.update_display()

    def add_argument_against(self):
        argument = self.arg_input_button.text()
        self.arguments_against.append(argument)
        self.save_data()
        self.update_display()

    def update_display(self):
        self.question_label.setText(self.current_question)
        self.arguments_for_list.clear()
        self.arguments_against_list.clear()
        for argument in self.arguments_for:
            self.arguments_for_list.addItem(argument)
        for argument in self.arguments_against:
            self.arguments_against_list.addItem(argument)
        self.for_count = len(self.arguments_for_list)
        self.against_count = len(self.arguments_against_list)
        self.for_count_button.setText('Количество за: ' + str(self.for_count))
        self.against_count_button.setText('Количество против : ' + str(self.against_count))


    def reset_all(self):
        self.current_question = "Вопрос"
        self.question_input.clear()
        self.arguments_for.clear()
        self.arguments_against.clear()

        self.save_data()
        self.update_display()

    def load_data(self):
        try:
            with open("/Users/arseniy/Documents/GitHub/UID/JSONки/Сохранение 2 минипроекта.json", "r") as file:
                data = json.load(file)
                self.arguments_for = data["arguments_for"]
                self.arguments_against = data["arguments_against"]
                self.for_count = data["for_count"]
                self.against_count = data["against_count"]
                self.current_question = data["current_question"]
        except FileNotFoundError:
            pass
        

    def save_data(self):
        with open("/Users/arseniy/Documents/GitHub/UID/JSONки/Сохранение 2 минипроекта.json", "w") as file:
            json.dump({"arguments_for": self.arguments_for,
                       "arguments_against": self.arguments_against,
                       "for_count": self.for_count,
                       "against_count": self.against_count,
                       "current_question": self.current_question}, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
    
    
    
    
    
    
    
    
    
    
    
    