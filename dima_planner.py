import sys
import json
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QDateTime


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('files/MainWindow.ui', self)
        self.view_left.setIcon(QIcon('files/arrow_left.png'))
        self.view_right.setIcon(QIcon('files/arrow_right.png'))
        self.setFixedSize(1045, 600)
        self.table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)

        self.current_date = self.calendar.selectedDate()
        self.interval = "day"
        self.update_label()

        self.events = {}
        self.load_events()
        self.update_event()
        self.day()
        self.main()

    def main(self):
        self.view_day.clicked.connect(self.day)
        self.view_week.clicked.connect(self.week)
        self.view_month.clicked.connect(self.month)
        self.view_right.clicked.connect(self.right_func)
        self.view_left.clicked.connect(self.left_func)
        self.calendar.selectionChanged.connect(self.update_event)
        self.calendar.selectionChanged.connect(self.update_label)
        self.action_create.clicked.connect(self.add_event)
        self.action_delete.clicked.connect(self.remove_event)

    def day(self):
        self.table.setColumnCount(1)
        self.table.setColumnWidth(0, 800)
        self.table.setRowCount(24)
        self.table.setHorizontalHeaderLabels(['День'])
        self.table.setVerticalHeaderLabels(['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'])
        self.interval = 'day'
        self.update_label()

    def week(self):
        self.table.setColumnCount(7)
        for _ in range(8):
            self.table.setColumnWidth(_, 100)
        self.table.setRowCount(24)
        self.table.setHorizontalHeaderLabels(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'])
        self.table.setVerticalHeaderLabels(['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'])
        self.interval = 'week'
        self.update_label()

    def month(self):
        self.table.setColumnCount(7)
        for _ in range(8):
            self.table.setColumnWidth(_, 107)
        self.table.setRowCount(5)
        self.table.setHorizontalHeaderLabels(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'])
        self.table.setVerticalHeaderLabels(['', '', '', '', ''])
        self.interval = 'month'
        self.update_label()

    def change_interval(self, interval):
        self.interval = interval
        self.update_label()

    def left_func(self):
        if self.interval == "day":
            self.current_date = self.current_date.addDays(-1)
        elif self.interval == "week":
            self.current_date = self.current_date.addDays(-7)
        elif self.interval == "month":
            self.current_date = self.current_date.addMonths(-1)
        self.calendar.setSelectedDate(self.current_date)
        self.update_label()

    def right_func(self):
        if self.interval == "day":
            self.current_date = self.current_date.addDays(1)
        elif self.interval == "week":
            self.current_date = self.current_date.addDays(7)
        elif self.interval == "month":
            self.current_date = self.current_date.addMonths(1)
        self.calendar.setSelectedDate(self.current_date)
        self.update_label()

    def update_label(self):
        selected_date = self.calendar.selectedDate()
        if self.interval == "day":
            self.date_table.setText(selected_date.toString("dd.MM.yyyy"))
        elif self.interval == "week":
            start_of_week = selected_date.addDays(-selected_date.dayOfWeek() + 1)
            end_of_week = start_of_week.addDays(6)
            self.date_table.setText(f"{start_of_week.toString('dd.MM.yyyy')} - {end_of_week.toString('dd.MM.yyyy')}")
        elif self.interval == "month":
            start_of_month = selected_date.addDays(-selected_date.day() + 1)
            end_of_month = start_of_month.addMonths(1).addDays(-1)
            self.date_table.setText(f"{start_of_month.toString('dd.MM.yyyy')} - {end_of_month.toString('dd.MM.yyyy')}")

    def add_event(self):
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("dd.MM.yyyy")

        dialog = AddEventDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            event_text, event_time = dialog.get_event_data()
            datetime_str = QDateTime(selected_date, event_time).toString("dd.MM.yyyy hh:mm")
            if date_str in self.events:
                self.events[date_str].append((event_text, datetime_str))
            else:
                self.events[date_str] = [(event_text, datetime_str)]
            self.update_event()
            self.save_events()

    def update_event(self):
        self.action_list.clear()
        for i in range(3):
            selected_date = self.calendar.selectedDate().addDays(i)
            date_str = selected_date.toString("dd.MM.yyyy")
            if date_str in self.events:
                events = sorted(self.events[date_str], key=lambda x: x[1])
                if len(events) > 0:
                    item = QtWidgets.QListWidgetItem(selected_date.toString("d MMMM yyyy"))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    self.action_list.addItem(item)
                    for event in events:
                        self.action_list.addItem(event[0] + " - " + event[1])

    def load_events(self):
        try:
            with open('files/events.json', 'r') as file:
                self.events = json.load(file)
        except FileNotFoundError:
            pass

    def save_events(self):
        with open('files/events.json', 'w') as file:
            json.dump(self.events, file)

    def remove_event(self):
        selected_item = self.action_list.currentItem()
        if selected_item:
            selected_event = selected_item.text().split(" - ")[0]
            selected_date = self.calendar.selectedDate()
            date_str = selected_date.toString("dd.MM.yyyy")
            if date_str in self.events:
                self.events[date_str] = [event for event in self.events[date_str] if event[0] != selected_event]
                self.update_event()
                self.save_events()


class AddEventDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить событие")

        layout = QtWidgets.QVBoxLayout()

        self.event_text_edit = QtWidgets.QTextEdit()
        layout.addWidget(self.event_text_edit)

        self.time_edit = QtWidgets.QTimeEdit()
        layout.addWidget(self.time_edit)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_event_data(self):
        event_text = self.event_text_edit.toPlainText()
        event_time = self.time_edit.time()
        return event_text, event_time


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
