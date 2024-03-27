import sys
from PyQt6 import uic  
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Минипроект ч. 2.ui', self)  

        self.initUI()

    def initUI(self):
        self.count_for = 0
        self.count_against = 0

        self.btn_reset.clicked.connect(self.reset_counts)

        self.input_decision.setPlaceholderText('Что нужно решить?')
        self.input_arguments.setPlaceholderText('Введите аргумент')
        
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.btn_for)
        hbox_buttons.addWidget(self.btn_against)
        hbox_buttons.addWidget(self.btn_reset)

        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.input_decision)
        vbox_main.addWidget(self.label_for)
        vbox_main.addWidget(self.label_against)
        vbox_main.addWidget(self.input_arguments)
        vbox_main.addLayout(hbox_buttons)

        self.setLayout(vbox_main)

        self.btn_for.clicked.connect(self.increment_for)
        self.btn_against.clicked.connect(self.increment_against)

        self.load_votes()

    def increment_for(self):
        self.count_for += 1
        self.update_labels()
        self.save_votes()

    def increment_against(self):
        self.count_against += 1
        self.update_labels()
        self.save_votes()

    def reset_counts(self):
        self.count_for = 0
        self.count_against = 0
        self.update_labels()
        self.save_votes()

    def update_labels(self):
        self.label_for.setText(f'За: {self.count_for}')
        self.label_against.setText(f'Против: {self.count_against}')

    def save_votes(self):
        with open('votes.txt', 'w') as file:
            file.write(f'За: {self.count_for}\n')
            file.write(f'Против: {self.count_against}\n')
            decision_text = self.input_decision.text()
            file.write(f'Решение: {decision_text}\n')
            question_text = self.input_decision.text()
            file.write(f'Вопрос: {question_text}\n')
            argument_text = self.input_arguments.text()
            if argument_text:
                file.write(f'Аргумент: {argument_text}\n')

    def load_votes(self):
        try:
            with open('votes.txt', 'r') as file:
                lines = file.readlines()
                self.count_for = int(lines[0].split(': ')[1])
                self.count_against = int(lines[1].split(': ')[1])
                decision_text = lines[2].split(': ')[1].strip()
                self.update_labels()
                self.input_decision.setText(decision_text)
                question_text = lines[3].split(': ')[1].strip()
                self.input_question.setText(question_text)
                if len(lines) > 4:
                    argument_text = lines[4].split(': ')[1].strip()
                    self.input_arguments.setText(argument_text)
        except FileNotFoundError:
            print("Файл с голосами не найден.")
        except Exception as e:
            print("Ошибка загрузки голосов:", e)
    def closeEvent(self, event):
        self.save_votes()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())