import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage, QTransform
from PyQt6.QtCore import Qt, QTimer

class ImageSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)
        
        self.timer = QTimer()
        self.images = []
        self.current_idx = 0
        
        self.load_images()
        self.update_image()
        
    def load_images(self):
        formats = ['jpg', 'png']
        dirname = QFileDialog.getExistingDirectory(self, 'Выберите папку с изображениями')
        for filename in os.listdir(dirname):
            if filename.split('.')[-1].lower() in formats:
                self.images.append(os.path.join(dirname, filename))
        
        self.current_idx = 0
        
    def update_image(self):
        pixmap = QPixmap(self.images[self.current_idx])
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
        
    def next_image(self):
        self.current_idx = (self.current_idx + 1) % len(self.images)
        self.update_image()
        
    def previous_image(self):
        self.current_idx = (self.current_idx - 1) % len(self.images)
        self.update_image()
        
    def rotate_image(self):
        transform = QTransform().rotate(90)
        pixmap = self.image_label.pixmap().transformed(transform)
        self.image_label.setPixmap(pixmap)
        
    def delete_image(self):
        os.remove(self.images[self.current_idx])
        self.images.pop(self.current_idx)
        if self.current_idx >= len(self.images):
            self.current_idx = len(self.images) - 1
        self.update_image()

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.image_slider = ImageSlider()
        self.setCentralWidget(self.image_slider)
        
        self.controls_layout = QVBoxLayout()
        next_button = QPushButton('Вперед', self)
        next_button.clicked.connect(self.image_slider.next_image)
        self.controls_layout.addWidget(next_button)
        
        previous_button = QPushButton('Назад', self)
        previous_button.clicked.connect(self.image_slider.previous_image)
        self.controls_layout.addWidget(previous_button)
        
        rotate_button = QPushButton('Повернуть', self)
        rotate_button.clicked.connect(self.image_slider.rotate_image)
        self.controls_layout.addWidget(rotate_button)
        
        delete_button = QPushButton('Удалить', self)
        delete_button.clicked.connect(self.image_slider.delete_image)
        self.controls_layout.addWidget(delete_button)
        
        self.controls_widget = QWidget()
        self.controls_widget.setLayout(self.controls_layout)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.controls_widget)
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())
