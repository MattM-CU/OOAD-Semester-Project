# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
from numpy import ndarray
from db_connect import Database
from video_streamer import VideoStreamer
from face_recognizer import FaceRecognizer
import cv2


class AppEngine(QObject):

	# SIGNALS GO HERE
	changeFrame = pyqtSignal(ndarray)

	def __init__(self):

		super().__init__()

		# self.database = Database()
		# todo - make sure database is created here


		self.videoStreamer = VideoStreamer()

		# todo - connect change frame signal to appropriate method
		self.videoStreamer.newPiFrame.connect(self.faceRecognizeFrame)

		# todo - make the face recognizer
		self.faceRecognizer = FaceRecognizer()

	def connectToPi(self, pi_address):

		self.videoStreamer.setPiAddress(pi_address)

		self.videoStreamer.start()

	@pyqtSlot(ndarray)
	def faceRecognizeFrame(self, cv_img):

		overlayed_img = self.faceRecognizer.findImageFaces(cv_img)

		self.changeFrame.emit(overlayed_img)



		




