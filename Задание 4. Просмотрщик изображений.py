import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog
from PyQt6.QtGui import QPixmap

SCREEN_SIZE = [500, 500]

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение картинки')

        fname, _ = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '','Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')
        self.pixmap = QPixmap(fname)
        if not self.pixmap.isNull():
            self.image = QLabel(self)
            self.image.move(60, 60)
            self.image.resize(400, 400)
            self.image.setPixmap(self.pixmap)
        else:
            self.statusBar().showMessage('Выберите файл изображения')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec()) 