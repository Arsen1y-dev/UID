import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QImage, QTransform
from PyQt6.QtCore import QTimer, Qt


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image_index = 0
        self.image_files = []
        self.image_count = 0

        self.setup_ui()
        self.load_images()
        self.update_image()

    def setup_ui(self):
        self.setWindowTitle("Image Viewer")
        self.central_widget = QLabel()
        self.setCentralWidget(self.central_widget)

        self.btn_previous = QPushButton("Previous", self)
        self.btn_previous.clicked.connect(self.previous_image)

        self.btn_next = QPushButton("Next", self)
        self.btn_next
