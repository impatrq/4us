from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QMovie
from time import sleep
import threading

class GifPlayer (QWidget):
    def __init__(self,GIF):
        super().__init__()
        self.setGeometry(-1,-1,1800,1200)

        label = QLabel(self)
        movie = QMovie(GIF) #tamaño correcto de gif -> 1280 x 720
        label.setMovie(movie)
        movie.start()

def gif_closer(time: int, app: QApplication, gif_player: GifPlayer) -> None:
    """
    --Description--

    Params:
        time: delay time in seconds
        app: QApplication instance
        gif_player: GifPlayer instance
    """
    sleep(time)
    gif_player.hide()
    return app.quit()


GIF_LIST = ['big.gif','city.gif','car.gif']

APP = QApplication([])
gif_players = [GifPlayer(GIF) for GIF in GIF_LIST]

for gif_player in gif_players:
    gif_player.show()
    gif_end = threading.Thread(target = gif_closer, args = [2, APP, gif_player])
    gif_end.start()
    APP.exec()
    gif_end.join()