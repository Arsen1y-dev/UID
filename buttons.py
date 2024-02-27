import sys

from PyQt5 import QtWidgets


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.SIZE = (300, 90)
        self.cnt = 0
        self.setWindowTitle("Программа на PyQt")
        self.resize(*self.SIZE)
        self.label = QtWidgets.QLabel("Пpивeт, мир!", self)
        self.btn = QtWidgets.QPushButton("&Зaкpыть окно", self)
        self.btn.move((self.width() - self.btn.width()) // 2, 30)
        self.btn.clicked.connect(self.who_sent)
        self.btnCnt = QtWidgets.QPushButton("Нажми меня!", self)
        self.btnCnt.move((self.width() - self.btnCnt.width()) // 2, 60)
        self.btnCnt.clicked.connect(self.who_sent)
        self.show()

    def move_btn(self):
        self.btn.move((self.btn.x() + 5) % (self.width() - self.btn.width()), 30)

    def add_cnt(self):
        self.cnt += 1
        self.label.setText(f"Пpивeт, мир! {self.cnt}")
        self.label.adjustSize()

    def who_sent(self):
        # if self.sender() is self.btn:
        #     self.label.setText("Одна кнопка")
        # else:
        #     self.label.setText("Другая кнопка")
        self.label.setText(self.sender().text())
        self.label.adjustSize()


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())
