import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCalendarWidget, QPushButton, QTextEdit, \
    QDialog, QDialogButtonBox, QListWidget, QMessageBox, QHBoxLayout, QTimeEdit, QListWidgetItem
from PyQt6.QtCore import QDateTime, QDate, Qt


class AddEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить событие")

        layout = QVBoxLayout()

        self.event_text_edit = QTextEdit()
        layout.addWidget(self.event_text_edit)

        self.time_edit = QTimeEdit()
        layout.addWidget(self.time_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_event_data(self):
        event_text = self.event_text_edit.toPlainText()
        event_time = self.time_edit.time()
        return event_text, event_time


class DayPlanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Планировщик дней")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_event)
        self.layout.addWidget(self.calendar)

        self.event_list = QListWidget()
        self.layout.addWidget(self.event_list)

        self.add_event_button = QPushButton("Добавить событие")
        self.add_event_button.clicked.connect(self.add_event)
        self.layout.addWidget(self.add_event_button)

        self.remove_event_button = QPushButton("Удалить событие")
        self.remove_event_button.clicked.connect(self.remove_event)
        self.layout.addWidget(self.remove_event_button)

        self.events = {}
        self.load_events()

    def add_event(self):
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("dd.MM.yyyy")

        dialog = AddEventDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            event_text, event_time = dialog.get_event_data()
            datetime_str = QDateTime(selected_date, event_time).toString("dd.MM.yyyy hh:mm")
            if date_str in self.events:
                self.events[date_str].append((event_text, datetime_str))
            else:
                self.events[date_str] = [(event_text, datetime_str)]
            self.update_event()
            self.save_events()

    def remove_event(self):
        selected_item = self.event_list.currentItem()
        if selected_item:
            selected_event = selected_item.text()
            selected_date = self.calendar.selectedDate()
            date_str = selected_date.toString("dd.MM.yyyy")
            if date_str in self.events:
                self.events[date_str] = [event for event in self.events[date_str] if event[0] != selected_event]
                self.update_event()
                self.save_events()

    def update_event(self):
        self.event_list.clear()
        for i in range(3):
            selected_date = self.calendar.selectedDate().addDays(i)
            date_str = selected_date.toString("dd.MM.yyyy")
            if date_str in self.events:
                events = sorted(self.events[date_str], key=lambda x: x[1])
                if len(events) > 0:
                    item = QListWidgetItem(selected_date.toString("d MMMM yyyy"))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    self.event_list.addItem(item)
                    for event in events:
                        self.event_list.addItem(event[0] + " - " + event[1])

    def load_events(self):
        try:
            with open("events.json", "r") as file:
                self.events = json.load(file)
        except FileNotFoundError:
            pass

    def save_events(self):
        with open("events.json", "w") as file:
            json.dump(self.events, file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    planner = DayPlanner()
    planner.show()
    sys.exit(app.exec())
