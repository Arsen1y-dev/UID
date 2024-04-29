import sys

from PyQt6.QtWidgets import (QWidget, QApplication, QLabel,
                             QTabWidget, QPushButton, QVBoxLayout)


class Tab(QWidget):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.setText(f'Tab number {self.num}')
        self.lbl.move(5, 5)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вкладки')
        self.resize(400, 150)
        self.layout = QVBoxLayout(self)

        self.btn = QPushButton('Добавить вкладку')
        self.btn.clicked.connect(self.add_tab)
        self.layout.addWidget(self.btn)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        # self.tabs.addTab(Tab(self.tabs.count()), f'Tab {self.tabs.count()}')
        self.layout.addWidget(self.tabs)

    def add_tab(self):
        self.tabs.addTab(Tab(self.tabs.count()), f'Tab {self.tabs.count()}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
