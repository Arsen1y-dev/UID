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

        # Add buttons for special keys
        special_keys = ["Shift", "Caps Lock", "Backspace"]
        for key in special_keys:
            button = QPushButton(key)
            button.clicked.connect(lambda _, key=key: self.onSpecialKeyButtonClick(key))
            self.layout.addWidget(button)

        self.buttons = {}
        self.shift_pressed = False
        self.caps_lock = False

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

    def onSpecialKeyButtonClick(self, key):
        if key == "Shift":
            self.shift_pressed = not self.shift_pressed
        elif key == "Caps Lock":
            self.caps_lock = not self.caps_lock
        elif key == "Backspace":
            text = self.text_edit.text()
            self.text_edit.setText(text[:-1])

    def onButtonClick(self, letter):
        if self.shift_pressed or self.caps_lock:
            letter = letter.upper()
        self.text_edit.setText(self.text_edit.text() + letter)

def main():
    app = QApplication(sys.argv)
    window = VirtualKeyboard()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
