import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6 import uic  
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from datetime import datetime



class DailyPlanner(QMainWindow):
    def __init__(self):
        super(DailyPlanner, self).__init__()
        loadUi("Задание 3. Планировщик.ui", self)

        self.events = []

        self.addButton.clicked.connect(self.add_event)
        self.deleteButton.clicked.connect(self.delete_event)

    def add_event(self):
        event_name = self.eventLineEdit.text()
        date = self.calendarWidget.selectedDate()
        time = self.timeEdit.time()
        event_datetime = datetime.combine(date.toPyDate(), time.toPyTime())
        self.events.append((event_datetime, event_name))
        self.events.sort(key=lambda x: x[0])
        self.update_event_list()

    def delete_event(self):
        selected_items = self.eventList.selectedItems()
        if selected_items:
            reply = QMessageBox.question(self, 'Удалить событие', 'Вы уверены что хотите удалить это событие?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                for item in selected_items:
                    index = self.eventList.row(item)
                    del self.events[index]
                self.update_event_list()

    def update_event_list(self):
        self.eventList.clear()
        for event_datetime, event_name in self.events:
            formatted_date = event_datetime.strftime('%Y-%m-%d %H:%M')
            self.eventList.addItem(f"{formatted_date}: {event_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DailyPlanner()
    window.show()
    sys.exit(app.exec_())
