import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QCalendarWidget,
    QListWidget, QLabel, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import QDate


class FlightBookingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Покупка билетов")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.label = QLabel("Выберите дату для просмотра рейсов")
        self.main_layout.addWidget(self.label)

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.show_flights)
        self.main_layout.addWidget(self.calendar)

        self.flights_list = QListWidget()
        self.flights_list.itemClicked.connect(self.enable_purchase_button)
        self.main_layout.addWidget(self.flights_list)

        self.purchase_button = QPushButton("Купить билет")
        self.purchase_button.setEnabled(False)
        self.purchase_button.clicked.connect(self.purchase_ticket)
        self.main_layout.addWidget(self.purchase_button)

        self.flights_data = {
            "2024-06-07": [
                "Рейс 101: Москва - Санкт-Петербург",
                "Рейс 102: Москва - Казань",
                "Рейс 103: Москва - Екатеринбург"
            ],
            "2024-06-08": [
                "Рейс 201: Москва - Новосибирск",
                "Рейс 202: Москва - Владивосток",
                "Рейс 203: Москва - Самара"
            ],
            "2024-06-09": [
                "Рейс 301: Москва - Краснодар",
                "Рейс 302: Москва - Сочи",
                "Рейс 303: Москва - Уфа"
            ],
            # Добавьте больше данных о рейсах по необходимости
        }

        self.show_flights()

    def show_flights(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.flights_list.clear()
        self.purchase_button.setEnabled(False)

        flights = self.flights_data.get(selected_date, [])
        if flights:
            self.flights_list.addItems(flights)
        else:
            self.flights_list.addItem("Нет доступных рейсов на эту дату")

    def enable_purchase_button(self):
        self.purchase_button.setEnabled(True)

    def purchase_ticket(self):
        selected_flight = self.flights_list.currentItem().text()
        QMessageBox.information(self, "Покупка билета", f"Вы купили билет на {selected_flight}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlightBookingWindow()
    window.show()
    sys.exit(app.exec())
