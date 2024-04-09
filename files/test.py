import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('01.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.progressBar.setValue(min(100, self.progressBar.value() + 10))
        print(self.progressBar.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
