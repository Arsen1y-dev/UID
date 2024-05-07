import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QListWidget, QComboBox, QLCDNumber, QVBoxLayout, QHBoxLayout, QWidget

class DecisionMaker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.decision_data = {}
        self.current_decision_key = None
        self.load_data()
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Decision Maker")
        self.setGeometry(100, 100, 511, 423)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.qwestion_input = QLineEdit()
        self.layout.addWidget(self.qwestion_input)

        self.qwestion_add = QPushButton("Добавить вопрос")
        self.qwestion_add.clicked.connect(self.set_question)
        self.layout.addWidget(self.qwestion_add)

        self.comboBox = QComboBox()
        self.comboBox.addItems(self.decision_data.keys())
        self.comboBox.currentIndexChanged.connect(self.switch_question)
        
        self.layout.addWidget(self.comboBox)

        self.arg_input = QLineEdit()
        self.layout.addWidget(self.arg_input)

        self.btn_layout = QHBoxLayout()
        self.layout.addLayout(self.btn_layout)

        self.arg_za = QPushButton("Добавить аргумент 'за'")
        self.arg_za.clicked.connect(self.add_argument_for)
        self.btn_layout.addWidget(self.arg_za)

        self.arp_prot = QPushButton("Добавить аргумент 'против'")
        self.arp_prot.clicked.connect(self.add_argument_against)
        self.btn_layout.addWidget(self.arp_prot)

        self.args_layout = QHBoxLayout()
        self.layout.addLayout(self.args_layout)

        self.args_za = QListWidget()
        self.args_layout.addWidget(self.args_za)

        self.args_prot = QListWidget()
        self.args_layout.addWidget(self.args_prot)

        self.lcd_layout = QHBoxLayout()
        self.layout.addLayout(self.lcd_layout)

        self.lcdNumber_za = QLCDNumber()
        self.lcd_layout.addWidget(self.lcdNumber_za)

        self.lcdNumber_protiv = QLCDNumber()
        self.lcd_layout.addWidget(self.lcdNumber_protiv)

        self.reset = QPushButton("Сброс")
        self.reset.clicked.connect(self.reset_all)
        self.layout.addWidget(self.reset)
        
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
            with open("/Users/arseniy/Documents/GitHub/UID/Минипроект ч. 4/Сохранение_4_минипроекта.json", "r") as file:
                self.decision_data = json.load(file)
        except FileNotFoundError:
            print(1)
            pass

    def save_data(self):
        with open("/Users/arseniy/Documents/GitHub/UID/Минипроект ч. 4/Сохранение_4_минипроекта.json", "w") as file:
            json.dump(self.decision_data, file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
