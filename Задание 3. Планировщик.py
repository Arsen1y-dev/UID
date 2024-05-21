import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QListWidgetItem
from PyQt6.QtCore import QDateTime, Qt
from PyQt6 import uic    

class AddEventDialog(QDialog):    
    def __init__(self, parent=None):        
        super().__init__(parent)
        uic.loadUi('/Users/arseniy/Documents/GitHub/UID/1,2,3 Задания/EventDialog.ui', self)  # Corrected path        

        self.buttonBox.accepted.connect(self.accept)        
        self.buttonBox.rejected.connect(self.reject)            

    def get_event_data(self):        
        event_text = self.textEdit.toPlainText()        
        event_time = self.timeEdit.time()        
        return event_text, event_time

class DayPlanner(QMainWindow):    
    def __init__(self):        
        super().__init__()
        uic.loadUi('/Users/arseniy/Documents/GitHub/UID/1,2,3 Задания/Задание 3. Планировщик.ui', self) # Corrected path               

        self.calendarWidget.selectionChanged.connect(self.update_event)
        self.addButton.clicked.connect(self.add_event)
        self.removeButton.clicked.connect(self.remove_event)
        self.events = {}
        self.load_events()
    
    def add_event(self):        
        selected_date = self.calendarWidget.selectedDate()
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
        selected_item = self.eventList.currentItem()
        if selected_item:            
            selected_text = selected_item.text().split(" - ")[0]  # Extract event text            
            selected_date = self.calendarWidget.selectedDate()
            date_str = selected_date.toString("dd.MM.yyyy")
            if date_str in self.events:
                self.events[date_str] = [event for event in self.events[date_str] if event[0] != selected_text]
                self.update_event()
                self.save_events()    

    def update_event(self):        
        self.eventList.clear()
        for i in range(3):            
            selected_date = self.calendarWidget.selectedDate().addDays(i)
            date_str = selected_date.toString("dd.MM.yyyy")
            if date_str in self.events:
                events = sorted(self.events[date_str], key=lambda x: x[1])
                if len(events) > 0:                    
                    item = QListWidgetItem(selected_date.toString("d MMMM yyyy"))                    
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)                    
                    self.eventList.addItem(item)                    
                    for event in events:                        
                        self.eventList.addItem(event[0] + " - " + event[1])    

    def load_events(self):        
        try:            
            with open("1,2,3 Задания/events.json", "r") as file: # Corrected path
                self.events = json.load(file)        
        except FileNotFoundError:            
            pass    

    def save_events(self):        
        with open("1,2,3 Задания/events.json", "w") as file: # Corrected path
            json.dump(self.events, file)

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    planner = DayPlanner()    
    planner.show()    
    sys.exit(app.exec())