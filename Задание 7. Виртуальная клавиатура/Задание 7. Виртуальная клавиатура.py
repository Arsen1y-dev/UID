import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QInputDialog


class VirtualKeyboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Virtual Keyboard")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.text_edit = QLineEdit()
        self.layout.addWidget(self.text_edit)

        self.buttons = {}

        self.show()

    def mouseDoubleClickEvent(self, event):
        button = QPushButton(self)
        button.setGeometry(event.pos().x(), event.pos().y(), 50, 50)
        letter, ok = QInputDialog.getText(self, "Input Dialog", "Enter a letter:")
        if ok:
            button.setText(letter)
            button.clicked.connect(lambda _, letter=letter: self.onButtonClick(letter))
            button.show()
            self.buttons[button] = letter

    def onButtonClick(self, letter):
        self.text_edit.setText(self.text_edit.text() + letter)


def main():
    app = QApplication(sys.argv)
    window = VirtualKeyboard()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
