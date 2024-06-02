import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, \
    QInputDialog, QGridLayout
from PyQt6.QtCore import Qt


class DraggableButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(50, 50)
        self.setCheckable(True)
        self.grid_size = 50
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet("background-color: lightgray; font-size: 18px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        self.move(self.mapToParent(event.pos() - self.drag_start_position))
        self.snap_to_grid()
        super().mouseMoveEvent(event)

    def snap_to_grid(self):
        x = round(self.x() / self.grid_size) * self.grid_size
        y = round(self.y() / self.grid_size) * self.grid_size
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() in {Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right}:
            self.navigate_focus(event.key())
        else:
            super().keyPressEvent(event)

    def navigate_focus(self, key):
        if not self.parent():
            return

        layout = self.parent().layout()
        current_index = layout.indexOf(self)
        total_buttons = layout.count()

        if key == Qt.Key.Key_Up:
            target_index = (current_index - 1) % total_buttons
        elif key == Qt.Key.Key_Down:
            target_index = (current_index + 1) % total_buttons
        elif key == Qt.Key.Key_Left:
            target_index = (current_index - 1) % total_buttons
        elif key == Qt.Key.Key_Right:
            target_index = (current_index + 1) % total_buttons
        else:
            return

        target_widget = layout.itemAt(target_index).widget()
        target_widget.setFocus()


class VirtualKeyboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.shift_pressed = False
        self.caps_lock = False

    def initUI(self):
        self.setWindowTitle("Virtual Keyboard")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.text_edit = QLineEdit()
        self.text_edit.setFixedHeight(50)
        self.text_edit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.main_layout.addWidget(self.text_edit)

        # Add a horizontal layout for special keys
        self.special_keys_layout = QHBoxLayout()
        special_keys = ["Shift", "Caps Lock", "Backspace"]
        for key in special_keys:
            button = QPushButton(key)
            button.setFixedSize(80, 50)
            button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            button.clicked.connect(lambda _, key=key: self.onSpecialKeyButtonClick(key))
            self.special_keys_layout.addWidget(button)

        self.main_layout.addLayout(self.special_keys_layout)

        self.keyboard_area = QWidget(self)
        self.keyboard_area.setStyleSheet("background-color: white; border: 1px solid black;")
        self.keyboard_area.setMouseTracking(True)
        self.keyboard_area.setLayout(QGridLayout())  # Используем сеточный макет для кнопок
        self.main_layout.addWidget(self.keyboard_area)

        self.show()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.create_button(event)

    def create_button(self, event):
        button = DraggableButton('', self.keyboard_area)
        button.setGeometry(event.pos().x(), event.pos().y(), 50, 50)
        letter, ok = QInputDialog.getText(self, "Input Dialog", "Enter a letter:")
        if ok:
            button.setText(letter)
            button.clicked.connect(lambda _, button=button, letter=letter: self.onButtonClick(button, letter))
            button.show()
            self.keyboard_area.layout().addWidget(button)  # Добавляем кнопку в макет

    def onSpecialKeyButtonClick(self, key):
        if key == "Shift":
            self.shift_pressed = not self.shift_pressed
        elif key == "Caps Lock":
            self.caps_lock = not self.caps_lock
        elif key == "Backspace":
            text = self.text_edit.text()
            self.text_edit.setText(text[:-1])

    def onButtonClick(self, button, letter):
        if self.shift_pressed or self.caps_lock:
            letter = letter.upper()
            if self.shift_pressed:
                self.shift_pressed = False
        self.text_edit.setText(self.text_edit.text() + letter)
        button.setChecked(False)

    def keyPressEvent(self, event):
        focused_widget = self.focusWidget()
        if isinstance(focused_widget, DraggableButton):
            focused_widget.keyPressEvent(event)
        elif event.key() in {Qt.Key.Key_Tab, Qt.Key.Key_Backtab}:
            self.navigate_focus(event)
        else:
            super().keyPressEvent(event)

    def navigate_focus(self, event):
        focus_widget = self.focusWidget()
        if event.key() == Qt.Key.Key_Tab:
            next_widget = focus_widget.nextInFocusChain()
            while not next_widget.isEnabled() or next_widget == focus_widget:
                next_widget = next_widget.nextInFocusChain()
            next_widget.setFocus()
        elif event.key() == Qt.Key.Key_Backtab:
            prev_widget = focus_widget.previousInFocusChain()
            while not prev_widget.isEnabled() or prev_widget == focus_widget:
                prev_widget = prev_widget.previousInFocusChain()
            prev_widget.setFocus()


def main():
    app = QApplication(sys.argv)
    window = VirtualKeyboard()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
