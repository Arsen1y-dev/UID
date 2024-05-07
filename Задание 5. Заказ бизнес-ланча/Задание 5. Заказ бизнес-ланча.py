import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, \
    QMessageBox, QButtonGroup, QCheckBox


class BusinessLunchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заказ бизнес-ланча")
        self.setGeometry(100, 100, 400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.menu_prices = {"Грибной крем-суп": 350, "Куриный суп": 300, "Том ям": 400,
                            "Жаркое из курицы с овощами": 400, "Роллы Филадельфия": 350,
                            "Лосось на спарже": 450,
                            "Цезарь с курицей": 200, "Салат с говядиной": 250, "Греческий салат с муссом фета": 200,
                            "Чизкейк": 200, "Мороженое": 100, "Молочный торт": 150,
                            "Зелёный чай": 120, "Чёрный чай": 120, "Смузи": 150, "Лимонад": 100
                            }
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.button_groups = []  # Список для хранения групп радиокнопок
        self.create_menu_options()
        self.order_button = QPushButton("Оформить заказ")
        self.order_button.clicked.connect(self.submit_order)
        self.layout.addWidget(self.order_button)

    def create_menu_options(self):
        options_layout = QVBoxLayout()
        soup_group = self.create_option_group("Супы",
                                              [f"Грибной крем-суп ({self.menu_prices['Грибной крем-суп']} руб.)",
                                               f"Куриный суп ({self.menu_prices['Куриный суп']} руб.)",
                                               f"Том ям ({self.menu_prices['Том ям']} руб.)"])
        options_layout.addLayout(soup_group)
        main_course_group = self.create_option_group("Горячее",
                                                     [
                                                         f"Жаркое из курицы с овощами ({self.menu_prices['Жаркое из курицы с овощами']} руб.)",
                                                         f"Роллы Филадельфия ({self.menu_prices['Роллы Филадельфия']} руб.)",
                                                         f"Лосось на спарже ({self.menu_prices['Лосось на спарже']} руб.)"])
        options_layout.addLayout(main_course_group)
        salad_group = self.create_option_group("Салат",
                                               [f"Цезарь с курицей ({self.menu_prices['Цезарь с курицей']} руб.)",
                                                f"Салат с говядиной ({self.menu_prices['Салат с говядиной']} руб.)",
                                                f"Греческий салат с муссом фета ({self.menu_prices['Греческий салат с муссом фета']} руб.)"])
        options_layout.addLayout(salad_group)
        dessert_group = self.create_option_group("Десерт", [f"Чизкейк ({self.menu_prices['Чизкейк']} руб.)",
                                                            f"Мороженое ({self.menu_prices['Мороженое']} руб.)",
                                                            f"Молочный торт ({self.menu_prices['Молочный торт']} руб.)"])
        options_layout.addLayout(dessert_group)
        drink_group = self.create_option_group("Напиток", [f"Зелёный чай ({self.menu_prices['Зелёный чай']} руб.)",
                                                           f"Чёрный чай ({self.menu_prices['Чёрный чай']} руб.)",
                                                           f"Смузи ({self.menu_prices['Смузи']} руб.)",
                                                           f"Лимонад ({self.menu_prices['Лимонад']} руб.)"])
        options_layout.addLayout(drink_group)
        self.layout.addLayout(options_layout)

    def create_option_group(self, name, options):
        group_layout = QVBoxLayout()
        group_label = QLabel(name)
        group_layout.addWidget(group_label)
        button_group = QButtonGroup(self)  # Создаем группу радиокнопок
        self.button_groups.append(button_group)  # Добавляем группу в список
        for option in options:
            option_radio = QRadioButton(option)
            group_layout.addWidget(option_radio)
            button_group.addButton(option_radio)
        return group_layout

    def submit_order(self):
        selected_options, total_price = self.get_selected_options()
        if len(selected_options) < 2:
            self.show_message_box("Ошибка", "Выберите не менее двух позиций для оформления заказа")
        else:
            order_summary = "\n".join(selected_options)
            order_summary += f"\n\nИтого: {total_price} руб."
            self.show_message_box("Заказ принят", f"Вы заказали:\n{order_summary}")

    def get_selected_options(self):
        selected_options = []
        total_price = 0
        for button_group in self.button_groups:
            if button_group.checkedButton() is not None:
                selected_options.append(button_group.checkedButton().text())
                dish = button_group.checkedButton().text().split(" (")[0]  # Извлекаем название блюда
                total_price += self.menu_prices.get(dish, 0)
        return selected_options, total_price

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()



app = QApplication(sys.argv)
window = BusinessLunchApp()
window.show()
sys.exit(app.exec())

