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
# import cv2
import pickle


class AppEngine(QObject):

	# SIGNALS GO HERE
	changeFrame = pyqtSignal(ndarray)

	def __init__(self):

		super().__init__()

		self.database = Database('../data/face_data.db')

		# ensure appropriate table is created
		create_sql = "CREATE TABLE IF NOT EXISTS faces (FaceName TEXT PRIMARY KEY," \
					 "FaceEncodings BLOB NOT NULL)"
		self.database.createDatabase(create_sql)

		self.videoStreamer = VideoStreamer()
		self.videoStreamer.newPiFrame.connect(self.faceRecognizeFrame)

		self.faceRecognizer = FaceRecognizer()

		self.alertObserver = None  # TODO

	def connectToPi(self, pi_address):

		self.videoStreamer.setPiAddress(pi_address)

		self.videoStreamer.start()

	@pyqtSlot(ndarray)
	def faceRecognizeFrame(self, cv_img):

		overlayed_img = self.faceRecognizer.findImageFaces(cv_img)

		self.changeFrame.emit(overlayed_img)

		# todo - check for unknown in names, signal observer if found

	def addFaceToDb(self, name, encodings):

		# name - str
		# encodings - list of lists
		encodings_bytes = pickle.dumps(encodings)

		sql = "INSERT INTO faces (FaceName, FaceEncodings) VALUES (?, ?)"

		self.database.executeNonQuery(sql, variables=[name, encodings_bytes])

	def deleteFaceFromDb(self, name):

		sql = "DELETE FROM faces WHERE FaceName = ?"

		self.database.executeNonQuery(sql, variables=[name])

