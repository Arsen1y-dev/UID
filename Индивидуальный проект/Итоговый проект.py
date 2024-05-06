import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import Qt

class PhotoSalon(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        user_button = QPushButton("User Management")
        user_button.clicked.connect(self.open_user_management)
        grid.addWidget(user_button, 0, 0)

        photo_gallery_button = QPushButton("Photo Gallery")
        photo_gallery_button.clicked.connect(self.open_photo_gallery)
        grid.addWidget(photo_gallery_button, 1, 0)

        order_tracking_button = QPushButton("Order Tracking")
        order_tracking_button.clicked.connect(self.open_order_tracking)
        grid.addWidget(order_tracking_button, 2, 0)

        self.show()

    def open_user_management(self):
        # Open user management UI
        pass

    def open_photo_gallery(self):
        # Open photo gallery UI
        pass

    def open_order_tracking(self):
        # Open order tracking UI
        pass

class UserManager:
    def __init__(self):
        self.users = []

    def create_user(self, username, password, email):
        new_user = {"username": username, "password": password, "email": email}
        self.users.append(new_user)
        return new_user

    def get_users(self):
        return self.users

    def delete_user(self, username):
        for user in self.users:
            if user["username"] == username:
                self.users.remove(user)
                return True
        return False


class PhotoGallery:
    def __init__(self):
        self.photos = []

    def add_photo(self, photo_id, title, description, image_path):
        new_photo = {"photo_id": photo_id, "title": title, "description": 
description, "image_path": image_path}
        self.photos.append(new_photo)
        return new_photo

    def get_photos(self):
        return self.photos

    def delete_photo(self, photo_id):
        for photo in self.photos:
            if photo["photo_id"] == photo_id:
                self.photos.remove(photo)
                return True
        return False


class OrderTracker:
    def __init__(self):
        self.orders = []

    def add_order(self, order_id, customer_name, order_date):
        new_order = {"order_id": order_id, "customer_name": customer_name, 
"order_date": order_date}
        self.orders.append(new_order)
        return new_order

    def get_orders(self):
        return self.orders

    def delete_order(self, order_id):
        for order in self.orders:
            if order["order_id"] == order_id:
                self.orders.remove(order)
                return True
        return False


class PhotoSalonUI(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)

        user_button = QPushButton("User Management")
        user_button.clicked.connect(self.open_user_management)
        grid.addWidget(user_button, 0, 0)

        photo_gallery_button = QPushButton("Photo Gallery")
        photo_gallery_button.clicked.connect(self.open_photo_gallery)
        grid.addWidget(photo_gallery_button, 1, 0)

        order_tracking_button = QPushButton("Order Tracking")
        order_tracking_button.clicked.connect(self.open_order_tracking)
        grid.addWidget(order_tracking_button, 2, 0)

        self.show()

    def open_user_management(self):
        user_management_window = UserManagementWindow()
        user_management_window.show()

    def open_photo_gallery(self):
        photo_gallery_window = PhotoGalleryWindow()
        photo_gallery_window.show()

    def open_order_tracking(self):
        order_tracking_window = OrderTrackingWindow()
        order_tracking_window.show()


def main():
    app = QApplication(sys.argv)
    salon = PhotoSalonUI()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()