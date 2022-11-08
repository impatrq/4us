import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from time import sleep


class LoadingGif(object):

	def mainUI(self, FrontWindow):
		FrontWindow.setObjectName("FTwindow")
		FrontWindow.resize(1024, 600)
		self.centralwidget = QtWidgets.QWidget(FrontWindow)
		self.centralwidget.setObjectName("main-widget")

		# Label Create
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(25, 25, 1024, 600))
		self.label.setMinimumSize(QtCore.QSize(1024, 600))
		self.label.setMaximumSize(QtCore.QSize(1024, 600))
		self.label.setObjectName("lb1")
		FrontWindow.setCentralWidget(self.centralwidget)
		# Loading the GIF
		self.movie = QMovie("loader.gif")
		self.label.setMovie(self.movie)

		self.startAnimation()

	# Start Animation

	def startAnimation(self):
		self.movie.start()

	# Stop Animation(According to need)
	def stopAnimation(self):
		self.movie.stop()

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
demo = LoadingGif()
demo.mainUI(window)
window.show()
sys.exit(app.exec_())
