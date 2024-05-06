import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Программа на PyQt")
        self.resize(500, 100)
        
        self.label = QtWidgets.QLabel("Привет, мир!", self)
        self.label.move(200, 10)
        
        self.btn_move = QtWidgets.QPushButton("Двигать", self)
        self.btn_move.setFixedWidth(100)
        self.btn_move.clicked.connect(self.move_btn)
        
        self.btn_counter = QtWidgets.QPushButton("0", self)
        self.btn_counter.clicked.connect(self.increment_counter)
        
        self.btn_yes = QtWidgets.QPushButton("ДА", self)
        self.btn_yes.clicked.connect(self.button_clicked)
        
        self.btn_no = QtWidgets.QPushButton("НЕТ", self)
        self.btn_no.clicked.connect(self.button_clicked)
        
        self.label_btn_text = QtWidgets.QLabel("", self)
        
        self.HBox = QtWidgets.QHBoxLayout()
        self.HBox.addWidget(self.btn_counter)
        self.HBox.addWidget(self.btn_yes)
        self.HBox.addWidget(self.btn_no)
        
        self.VBox = QtWidgets.QVBoxLayout(self)
        self.VBox.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.VBox.addWidget(self.label_btn_text, alignment=Qt.AlignmentFlag.AlignCenter)
        self.VBox.addLayout(self.HBox)
        self.VBox.addWidget(self.btn_move)
        
        
        self.counter = 0
        
        self.show()

    def move_btn(self):
        current_x = self.btn_move.pos().x()
        if current_x + 50 > self.size().width() - self.btn_move.size().width():
            current_x = 0
        else:
            current_x += 50

        self.btn_move.move(current_x, self.btn_move.pos().y())
        
        
    def increment_counter(self):
        self.counter += 1
        self.btn_counter.setText(str(self.counter))
        
    def button_clicked(self):
        sender = self.sender()
        if sender == self.btn_yes:
            self.label_btn_text.setText("ДА")
        elif sender == self.btn_no:
            self.label_btn_text.setText("НЕТ")

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())