import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QListWidget, QLCDNumber, QVBoxLayout, QHBoxLayout,
    QWidget, QTabWidget, QCheckBox, QDialog, QMessageBox, QFormLayout,
    QMenu, QFileDialog, QInputDialog
)
from PyQt6.QtGui import QAction, QDrag, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QMimeData, QTimer, QEvent


class DecisionMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.decision_data = {}
        self.current_decision_key = None
        self.user_data = {}
        self.current_user = None
        self.load_data()
        self.show_login_dialog()

    def init_ui(self):
        self.setWindowTitle("Decision Maker")
        self.setGeometry(100, 100, 511, 423)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Main Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")
        edit_menu = menubar.addMenu("Правка")
        help_menu = menubar.addMenu("Справка")

        # File Menu Actions
        new_question_action = QAction("Новый вопрос", self)
        new_question_action.setShortcut("Ctrl+N")
        new_question_action.triggered.connect(self.show_question_dialog)
        file_menu.addAction(new_question_action)

        load_action = QAction("Загрузить", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_data_dialog)
        file_menu.addAction(load_action)

        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        undo_action = QAction("Отмена", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        help_action = QAction("Справка", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help_dialog)
        help_menu.addAction(help_action)

        self.qwestion_add = QPushButton("Добавить вопрос")
        self.qwestion_add.clicked.connect(self.show_question_dialog)
        self.layout.addWidget(self.qwestion_add)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.switch_question)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Add tabs for existing questions
        for question in self.decision_data.get(self.current_user, {}):
            self.add_tab(question)

        if not self.tab_widget.count():
            self.add_tab("Placeholder")  # This will add a blank tab

        # Update the display after loading questions
        self.update_display()


        # Shortcuts
        QShortcut(QKeySequence(Qt.Key.Key_Delete), self.tab_widget, self.delete_tab,
                  context=Qt.ShortcutContext.ApplicationShortcut)
        QShortcut(QKeySequence(Qt.Key.Key_N), self.tab_widget, self.show_question_dialog,
                  context=Qt.ShortcutContext.ApplicationShortcut)

    def add_tab(self, question):
        tab = QWidget()
        tab_layout = QVBoxLayout()

        arg_input = QLineEdit()
        btn_layout = QHBoxLayout()
        args_layout = QHBoxLayout()
        lcd_layout = QHBoxLayout()
        reset_button = QPushButton("Сброс")
        decision_made_checkbox = QCheckBox("Решение принято")

        arg_za = QPushButton("Добавить аргумент 'за'")
        arg_za.setObjectName("arg_za")
        arg_za.clicked.connect(self.add_argument_for)
        btn_layout.addWidget(arg_za)

        arp_prot = QPushButton("Добавить аргумент 'против'")
        arp_prot.setObjectName("arp_prot")
        arp_prot.clicked.connect(self.add_argument_against)
        btn_layout.addWidget(arp_prot)

        args_za = QListWidget()
        args_za.setObjectName("args_za")
        args_za.setDragEnabled(True)
        args_za.setAcceptDrops(True)
        args_za.itemDoubleClicked.connect(self.delete_argument)
        args_layout.addWidget(args_za)

        args_prot = QListWidget()
        args_prot.setObjectName("args_prot")
        args_prot.setDragEnabled(True)
        args_prot.setAcceptDrops(True)
        args_prot.itemDoubleClicked.connect(self.delete_argument)
        args_layout.addWidget(args_prot)

        lcdNumber_za = QLCDNumber()
        lcdNumber_za.setObjectName("lcdNumber_za")
        lcd_layout.addWidget(lcdNumber_za)

        lcdNumber_protiv = QLCDNumber()
        lcdNumber_protiv.setObjectName("lcdNumber_protiv")
        lcd_layout.addWidget(lcdNumber_protiv)

        reset_button.clicked.connect(self.reset_all)
        decision_made_checkbox.stateChanged.connect(self.handle_decision_made)

        tab_layout.addWidget(arg_input)
        tab_layout.addLayout(btn_layout)
        tab_layout.addLayout(args_layout)
        tab_layout.addLayout(lcd_layout)
        tab_layout.addWidget(reset_button)
        tab_layout.addWidget(decision_made_checkbox)

        tab.setLayout(tab_layout)
        self.tab_widget.addTab(tab, question)

        args_za.installEventFilter(self)
        args_prot.installEventFilter(self)

    def switch_question(self, index):
        if index >= 0:
            self.current_decision_key = self.tab_widget.tabText(index)
        else:
            self.current_decision_key = None
        self.update_display()

    def show_question_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить новый вопрос")
        layout = QVBoxLayout(dialog)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(lambda: self.set_question(input_field.text(), dialog))
        layout.addWidget(add_button)

        dialog.exec()

    def set_question(self, new_question, dialog):
        if new_question and new_question not in self.decision_data.get(self.current_user, {}):
            if self.current_user not in self.decision_data:
                self.decision_data[self.current_user] = {}
            self.decision_data[self.current_user][new_question] = {"arguments_for": [], "arguments_against": []}
            self.add_tab(new_question)
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
            self.current_decision_key = new_question
            self.save_data()
        dialog.accept()

    def add_argument_for(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            arg_input = current_tab.findChild(QLineEdit)
            argument = arg_input.text()
            self.decision_data[self.current_user][self.current_decision_key]["arguments_for"].append(argument)
            self.save_data()
            self.update_tab_display(current_tab)
            arg_input.clear()

    def add_argument_against(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            arg_input = current_tab.findChild(QLineEdit)
            argument = arg_input.text()
            self.decision_data[self.current_user][self.current_decision_key]["arguments_against"].append(argument)
            self.save_data()
            self.update_tab_display(current_tab)
            arg_input.clear()

    def update_display(self):
        if self.current_decision_key:
            current_tab = self.tab_widget.currentWidget()
            self.update_tab_display(current_tab)

    def update_tab_display(self, tab):
        args_za = tab.findChild(QListWidget, name="args_za")
        args_prot = tab.findChild(QListWidget, name="args_prot")
        lcdNumber_za = tab.findChild(QLCDNumber, name="lcdNumber_za")
        lcdNumber_protiv = tab.findChild(QLCDNumber, name="lcdNumber_protiv")

        current_data = self.decision_data[self.current_user].get(self.current_decision_key,
                                                                 {"arguments_for": [], "arguments_against": []})
        args_za.clear()
        args_prot.clear()
        for argument in current_data["arguments_for"]:
            args_za.addItem(argument)
        for argument in current_data["arguments_against"]:
            args_prot.addItem(argument)
        lcdNumber_za.display(len(current_data["arguments_for"]))
        lcdNumber_protiv.display(len(current_data["arguments_against"]))

        decision_made_checkbox = tab.findChild(QCheckBox)
        decision_made_checkbox.setEnabled(True)

    def update_lcd_counts(self):
        if self.current_decision_key:
            current_data = self.decision_data[self.current_user][self.current_decision_key]
            self.lcdNumber_za.display(len(current_data["arguments_for"]))
            self.lcdNumber_protiv.display(len(current_data["arguments_against"]))
        else:
            self.lcdNumber_za.display(0)
            self.lcdNumber_protiv.display(0)

    def handle_decision_made(self, state):
        current_tab = self.tab_widget.currentWidget()
        arg_input = current_tab.findChild(QLineEdit)
        arg_za = current_tab.findChild(QPushButton, name="arg_za")
        arp_prot = current_tab.findChild(QPushButton, name="arp_prot")
        reset_button = current_tab.findChild(QPushButton)

        if state:
            arg_input.setEnabled(False)
            if arg_za is not None:
                arg_za.setEnabled(False)
            if arp_prot is not None:
                arp_prot.setEnabled(False)
            if reset_button is not None:
                reset_button.setEnabled(False)
        else:
            arg_input.setEnabled(True)
            if arg_za is not None:
                arg_za.setEnabled(True)
            if arp_prot is not None:
                arp_prot.setEnabled(True)
            if reset_button is not None:
                reset_button.setEnabled(True)

    def reset_all(self):
        if self.current_decision_key:
            reply = QMessageBox.question(self, 'Подтвердите сброс', 'Вы уверены, что хотите сбросить текущий вопрос?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                current_index = self.tab_widget.currentIndex()
                self.tab_widget.removeTab(current_index)
                if self.current_user in self.decision_data and self.current_decision_key in self.decision_data[
                    self.current_user]:
                    del self.decision_data[self.current_user][self.current_decision_key]

                if self.tab_widget.count() > 0:
                    self.current_decision_key = self.tab_widget.tabText(self.tab_widget.currentIndex())
                else:
                    self.current_decision_key = None

                self.update_display()
                self.save_data()

    def load_data(self):
        try:
            with open("Сохранение_6_минипроекта.json", "r") as file:
                data = json.load(file)
                self.decision_data = data.get("decisions", {})
                self.user_data = data.get("users", {})
        except FileNotFoundError:
            print("Файл данных не найден.")
            pass

    def save_data(self):
        with open("Сохранение_6_минипроекта.json", "w") as file:
            json.dump({"decisions": self.decision_data, "users": self.user_data}, file)

    def show_login_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Авторизация")

        layout = QFormLayout(dialog)

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Имя пользователя:", username_input)
        layout.addRow("Пароль:", password_input)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(lambda: self.handle_login(username_input.text(), password_input.text(), dialog))
        layout.addWidget(login_button)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(
            lambda: self.handle_register(username_input.text(), password_input.text(), dialog))
        layout.addWidget(register_button)

        dialog.exec()

    def handle_login(self, username, password, dialog):
        if username in self.user_data and self.user_data[username] == password:
            self.current_user = username
            self.init_ui()
            dialog.accept()
        else:
            QMessageBox.warning(self, "Ошибка авторизации", "Неверное имя пользователя или пароль.")

    def handle_register(self, username, password, dialog):
        if username not in self.user_data:
            self.user_data[username] = password
            self.save_data()
            QMessageBox.information(self, "Регистрация успешна", "Теперь вы можете войти в систему.")
        else:
            QMessageBox.warning(self, "Ошибка регистрации", "Пользователь с таким именем уже существует.")

    def show_help_dialog(self):
        QMessageBox.information(self, "Справка", "Приложение для помощи в принятии решений. \n\n"
                                                 "Функции:\n"
                                                 "- Добавление вопросов.\n"
                                                 "- Добавление аргументов 'за' и 'против'.\n"
                                                 "- Подсчет аргументов.\n"
                                                 "- Отметка о принятии решения.\n"
                                                 "- Сброс вопроса.\n"
                                                 "- Перетаскивание аргументов между столбцами.\n"
                                                 "- Удаление аргументов и вопросов.\n"
                                                 "- Сохранение и загрузка данных.")

    def load_data_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить данные", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, "r") as file:
                    data = json.load(file)
                    self.decision_data = data.get("decisions", {})
                    self.user_data = data.get("users", {})
                    self.init_ui()
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Ошибка", "Неверный формат файла.")
            except FileNotFoundError:
                QMessageBox.warning(self, "Ошибка", "Файл не найден.")

    def delete_tab(self):
        if self.current_decision_key:
            reply = QMessageBox.question(self, 'Подтвердите удаление', 'Вы уверены, что хотите удалить текущий вопрос?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                current_index = self.tab_widget.currentIndex()
                self.tab_widget.removeTab(current_index)
                if self.current_user in self.decision_data and self.current_decision_key in self.decision_data[
                    self.current_user]:
                    del self.decision_data[self.current_user][self.current_decision_key]
                self.save_data()

    def delete_argument(self, item):
        current_tab = self.tab_widget.currentWidget()
        list_widget = self.sender()
        if self.current_decision_key:
            reply = QMessageBox.question(self, 'Подтвердите удаление', 'Вы уверены, что хотите удалить этот аргумент?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if list_widget.objectName() == "args_za":
                    self.decision_data[self.current_user][self.current_decision_key]["arguments_for"].remove(
                        item.text())
                elif list_widget.objectName() == "args_prot":
                    self.decision_data[self.current_user][self.current_decision_key]["arguments_against"].remove(
                        item.text())
                self.save_data()
                self.update_tab_display(current_tab)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.DragEnter:
            if event.mimeData().hasFormat("text/plain"):
                event.acceptProposedAction()
            else:
                event.ignore()
        elif event.type() == QEvent.Type.Drop:
            source_list = self.sender()
            target_list = obj
            if source_list.objectName() != target_list.objectName():
                if self.current_decision_key:
                    item = source_list.currentItem()
                    if item:
                        text = item.text()
                        if source_list.objectName() == "args_za":
                            self.decision_data[self.current_user][self.current_decision_key]["arguments_for"].remove(
                                text)
                            self.decision_data[self.current_user][self.current_decision_key][
                                "arguments_against"].append(text)
                        elif source_list.objectName() == "args_prot":
                            self.decision_data[self.current_user][self.current_decision_key][
                                "arguments_against"].remove(text)
                            self.decision_data[self.current_user][self.current_decision_key]["arguments_for"].append(
                                text)
                        self.save_data()
                        self.update_tab_display(self.tab_widget.currentWidget())
                        QTimer.singleShot(100, lambda: source_list.takeItem(source_list.row(item)))
                event.acceptProposedAction()
            else:
                event.ignore()
        elif event.type() == QEvent.Type.DragMove:
            if event.mimeData().hasFormat("text/plain"):
                event.acceptProposedAction()
            else:
                event.ignore()
        return super().eventFilter(obj, event)

    def close_tab(self, index):
        reply = QMessageBox.question(self, 'Подтвердите удаление', 'Вы уверены, что хотите удалить эту вкладку?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            tab_text = self.tab_widget.tabText(index)
            if self.current_user in self.decision_data and tab_text in self.decision_data[self.current_user]:
                del self.decision_data[self.current_user][tab_text]
            self.tab_widget.removeTab(index)
            self.save_data()

    def contextMenuEvent(self, event):
        tab_index = self.tab_widget.tabBar().tabAt(event.pos())
        if tab_index != -1:
            tab_text = self.tab_widget.tabText(tab_index)
            menu = QMenu(self)

            rename_action = QAction("Переименовать", self)
            rename_action.triggered.connect(lambda: self.rename_tab(tab_index, tab_text))
            menu.addAction(rename_action)

            delete_action = QAction("Удалить", self)
            delete_action.triggered.connect(lambda: self.close_tab(tab_index))
            menu.addAction(delete_action)

            menu.exec(event.globalPos())
        else:
            pass

    def rename_tab(self, tab_index, tab_text):
        new_name, ok = QInputDialog.getText(self, "Переименовать вкладку", "Введите новое имя:")
        if ok and new_name and new_name != tab_text:
            if self.current_user in self.decision_data and tab_text in self.decision_data[self.current_user]:
                self.decision_data[self.current_user][new_name] = self.decision_data[self.current_user].pop(tab_text)
                self.save_data()
            self.tab_widget.setTabText(tab_index, new_name)
            self.current_decision_key = new_name
            self.update_display()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionMaker()
    window.show()
    sys.exit(app.exec())
