import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon, QPixmap, QTransform
from PyQt6.QtCore import QTimer
import os



path = '/Users/arseniy/Documents/GitHub/interface_py/Задание 4. Просмотрщик изображений/files'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(f'{path}/MainWindow.ui', self)
        self.setWindowTitle('PhotoViewer')
        self.back.setIcon(QIcon(f'{path}/back.png'))
        self.forward.setIcon(QIcon(f'{path}/forward.png'))
        self.open.setIcon(QIcon(f'{path}/openFile.png'))
        self.delete_2.setIcon(QIcon(f'{path}/deleteFile.png'))
        self.close.setIcon(QIcon(f'{path}/closePic.png'))
        self.exit.setIcon(QIcon(f'{path}/exit.png'))
        self.right.setIcon(QIcon(f'{path}/right.png'))
        self.left.setIcon(QIcon(f'{path}/left.png'))
        self.slideshow.setIcon(QIcon(f'{path}/play.png'))
        self.go_up.setIcon(QIcon(f'{path}/go_up.png'))
        self.go_down.setIcon(QIcon(f'{path}/go_down.png'))

        self.picFlag = False
        self.openFile = ''
        self.timer = QTimer()
        self.forward.setEnabled(False)
        self.back.setEnabled(False)

        self.main()

    def main(self):
        self.open.triggered.connect(self.openFunc)
        self.exit.triggered.connect(lambda: MainWindow.close(self))
        self.close.triggered.connect(self.closeFunc)
        self.right.triggered.connect(self.rightRotate)
        self.left.triggered.connect(self.leftRotate)
        self.delete_2.triggered.connect(self.deleteFunc)
        self.slideshow.triggered.connect(self.slideshow_time_func)
        self.forward.clicked.connect(self.next_photo)
        self.back.clicked.connect(self.prev_photo)
        self.timer.timeout.connect(self.slideshow_func)
        self.go_up.triggered.connect(self.go_up_func)
        self.go_down.triggered.connect(self.go_down_func)

    def openFunc(self):
        self.openFile = QtWidgets.QFileDialog.getOpenFileName(None, 'Открыть', '', '*.png *.jpeg *.ico *.svg *.jpg')[0]
        if self.openFile != '':
            self.pixmap = QPixmap(self.openFile)
            self.pixmap = self.pixmap.scaled(Image.open(self.openFile).size[0], Image.open(self.openFile).size[1])
            self.picture.setPixmap(self.pixmap)
            self.picFlag = True
            os.chdir(os.path.dirname(os.path.abspath(self.openFile)))
            self.files = os.listdir()
            self.openFileIndex = self.files.index(self.openFile.split('/')[-1])
            if self.openFileIndex == 0:
                self.back.setEnabled(False)
                self.forward.setEnabled(True)
            elif self.openFileIndex == len(self.files) - 1:
                self.forward.setEnabled(False)
                self.back.setEnabled(True)
            else:
                self.forward.setEnabled(True)
                self.back.setEnabled(True)
        else:
            pass

    def closeFunc(self):
        self.picture.setText('Выберете фото для отображения...')
        self.picFlag = False

    def rightRotate(self):
        if self.picFlag is True:
            self.pixmap = QPixmap(self.pixmap.transformed(QTransform().rotate(+90)))
            self.picture.setPixmap(self.pixmap)
        else:
            pass

    def leftRotate(self):
        if self.picFlag is True:
            self.pixmap = QPixmap(self.pixmap.transformed(QTransform().rotate(-90)))
            self.picture.setPixmap(self.pixmap)
        else:
            pass

    def deleteFunc(self):
        if self.picFlag is True:
            self.requestWindow = Request(self)
            self.requestWindow.show()
        else:
            pass

    def next_photo(self):
        self.openFileIndex += 1
        if self.openFileIndex <= len(self.files) - 1:
            self.back.setEnabled(True)
            self.openFile = os.path.abspath(self.files[self.openFileIndex])
            self.pixmap = QPixmap(self.openFile)
            self.pixmap = self.pixmap.scaled(Image.open(self.openFile).size[0], Image.open(self.openFile).size[1])
            self.picture.setPixmap(self.pixmap)
            if self.openFileIndex + 1 > len(self.files) - 1:
                self.forward.setEnabled(False)

    def prev_photo(self):
        self.openFileIndex -= 1
        if self.openFileIndex >= 0:
            self.forward.setEnabled(True)
            self.openFile = os.path.abspath(self.files[self.openFileIndex])
            self.pixmap = QPixmap(self.openFile)
            self.pixmap = self.pixmap.scaled(Image.open(self.openFile).size[0], Image.open(self.openFile).size[1])
            self.picture.setPixmap(self.pixmap)
            if self.openFileIndex - 1 < 0:
                self.back.setEnabled(False)

    def slideshow_time_func(self):
        if self.picFlag is True:
            # self.temp = self.openFile.split('/')[-1]
            # self.files.remove(self.temp)
            self.indexFile = 0
            self.timer.start(3000)
        else:
            pass

    def slideshow_func(self):
        self.openFile = os.path.abspath(self.files[self.indexFile])
        self.pixmap = QPixmap(self.openFile)
        self.pixmap = self.pixmap.scaled(Image.open(self.openFile).size[0], Image.open(self.openFile).size[1])
        self.picture.setPixmap(self.pixmap)
        self.indexFile += 1
        if self.indexFile == len(self.files):
            # self.files.append(self.temp)
            self.timer.stop()

    def go_down_func(self):
        if self.picFlag is True:
            self.openFile = os.path.abspath(self.files[-1])
            self.pixmap = QPixmap(self.openFile)
            self.pixmap = self.pixmap.scaled(Image.open(self.openFile).size[0], Image.open(self.openFile).size[1])
            self.picture.setPixmap(self.pixmap)
            self.forward.setEnabled(False)
            self.back.setEnabled(True)
        else:
            pass

    def go_up_func(self):
        if self.picFlag is True:
            self.openFile = os.path.abspath(self.files[0])
            self.pixmap = QPixmap(self.openFile)
            self.pixmap = self.pixmap.scaled(Image.open(self.openFile).size[0], Image.open(self.openFile).size[1])
            self.picture.setPixmap(self.pixmap)
            self.forward.setEnabled(True)
            self.back.setEnabled(False)
        else:
            pass



class Request(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        uic.loadUi(f'{path}/request.ui', self)

        self.buttonBox.accepted.connect(self.okFuncForDelete)

    def okFuncForDelete(self):
        self.parent.picture.setText('Выберете фото для отображения...')
        self.parent.picFlag = False
        os.remove(self.parent.openFile)
        self.parent.openFile = ''
        self.parent.files = []
        self.parent.forward.setEnabled(False)
        self.parent.back.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
