import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QListWidget, QLCDNumber, QVBoxLayout, QHBoxLayout,
    QWidget, QTabWidget, QCheckBox
)


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

        # Tab Widget for Questions
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.switch_question)

        # Add existing questions as tabs
        for question in self.decision_data:
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
        self.current_decision_key = self.tab_widget.tabText(index)
        self.update_display()

    def set_question(self):
        new_question = self.qwestion_input.text()
        if new_question and new_question not in self.decision_data:
            self.decision_data[new_question] = {"arguments_for": [], "arguments_against": []}
            self.add_tab(new_question)
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            self.current_decision_key = new_question
            self.save_data()
        self.qwestion_input.clear()

    def add_argument_for(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            arg_input = current_tab.findChild(QLineEdit)
            argument = arg_input.text()
            self.decision_data[self.current_decision_key]["arguments_for"].append(argument)
            self.save_data()
            self.update_tab_display(current_tab)  # Update the current tab's display
            arg_input.clear()

    def add_argument_against(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            arg_input = current_tab.findChild(QLineEdit)
            argument = arg_input.text()
            self.decision_data[self.current_decision_key]["arguments_against"].append(argument)
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

        current_data = self.decision_data[self.current_decision_key]
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
            current_data = self.decision_data[self.current_decision_key]
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
            self.qwestion_input.setEnabled(False)
            self.qwestion_add.setEnabled(False)
            arg_input.setEnabled(False)
            if arg_za is not None:
                arg_za.setEnabled(False)
            if arp_prot is not None:
                arp_prot.setEnabled(False)
            if reset_button is not None:
                reset_button.setEnabled(False)
        else:
            self.qwestion_input.setEnabled(True)
            self.qwestion_add.setEnabled(True)
            arg_input.setEnabled(True)
            if arg_za is not None:
                arg_za.setEnabled(True)
            if arp_prot is not None:
                arp_prot.setEnabled(True)
            if reset_button is not None:
                reset_button.setEnabled(True)

    def reset_all(self):
        if self.current_decision_key:
            current_index = self.tab_widget.currentIndex()
            self.tab_widget.removeTab(current_index)
            del self.decision_data[self.current_decision_key]

            # Update current_decision_key BEFORE calling update_display
            if self.tab_widget.count() > 0:
                self.current_decision_key = self.tab_widget.tabText(self.tab_widget.currentIndex())
            else:
                self.current_decision_key = None

            self.update_display()
            self.save_data()

    def update_display(self):
        if self.current_decision_key:  # Check if a question is selected
            current_tab = self.tab_widget.currentWidget()

    def load_data(self):
        try:
            with open("/Users/arseniy/Documents/GitHub/UID/Минипроект ч. 4,5,6/Сохранение_4_минипроекта.json", "r") as file:
                self.decision_data = json.load(file)
        except FileNotFoundError:
            print(1)
            pass

    def save_data(self):
        with open("/Users/arseniy/Documents/GitHub/UID/Минипроект ч. 4,5,6/Сохранение_4_минипроекта.json", "w") as file:
            json.dump(self.decision_data, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
