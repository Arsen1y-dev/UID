import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('/Users/arseniy/Documents/GitHub/UID/Задание 5. Заказ бизнес-ланча/radio.ui', self)

        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.label.setText(self.buttonGroup.checkedButton().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
