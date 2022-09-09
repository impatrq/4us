from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QIcon, QMovie
import sys

class Window (QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(600,300,125,105)

        label = QLabel(self)
        movie = QMovie('cul.gif')
        label.setMovie(movie)
        movie.start()

app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())