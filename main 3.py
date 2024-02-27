import sys

from PyQt6 import QtWidgets


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Программа на PyQt")
        self.resize(300, 70)
        self.label = QtWidgets.QLabel("Пpивeт, мир!", self)
        self.btn = QtWidgets.QPushButton("Нажми меня", self)
        self.btn.move(0, 30)
        self.btn.clicked.connect(self.move_btn)
        self.show()

    def move_btn(self):
        self.btn.move(self.btn.x() + 5, 30)


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())