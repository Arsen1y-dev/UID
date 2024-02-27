import sys

from PyQt6 import QtWidgets


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Программа на PyQt")
        self.resize(300, 70)
        self.label = QtWidgets.QLabel("Пpивeт, мир!", self)
        self.btnQuit = QtWidgets.QPushButton("&Зaкpыть окно", self)
        self.btnQuit.move(0, 30)
        self.btnQuit.clicked.connect(self.close)
        self.show()


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())
