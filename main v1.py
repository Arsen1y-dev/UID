import sys

from PyQt6 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Программа на PyQt")
window.resize(300, 70)
label = QtWidgets.QLabel("Пpивeт, миp!", window)
btnQuit = QtWidgets.QPushButton("&Закрыть окно", window)
btnQuit.move(0, 30)
btnQuit.clicked.connect(app.quit)
window.show()
sys.exit(app.exec())
