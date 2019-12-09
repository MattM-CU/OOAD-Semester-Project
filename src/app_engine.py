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

		self.performFacialRecognition = False

		self.currentFrame = None
		self.currentAddFaceName = None
		self.currentAddFaceEncodings = list()

		self.alertObserver = None  # TODO

	def setCurrentFrame(self, frame):

		self.currentFrame = frame

	def setCurrentAddFaceName(self, name):

		self.currentAddFaceName = name

	def setFacialRecognitionState(self, state_bool):

		self.performFacialRecognition = state_bool

	def getAllFaceInfoFromDb(self):

		face_names = list()
		face_encodings = list()

		sql = "SELECT * FROM faces"

		results = self.database.executeQuery(sql, variables=[])

		for row in results:

			current_face_encodings = pickle.loads(eval(row['FaceEncodings']))

			face_names = face_names + ([row['FaceName']] * len(current_face_encodings))

			# https://stackoverflow.com/questions/52890916/python3-unpickle-a-string-representation-of-bytes-object
			face_encodings = face_encodings + current_face_encodings

		# face encodings list needs to be flattened (b/c each sublist is only length 1)
		return face_names, [encoding[0] for encoding in face_encodings]

	def connectToPi(self, pi_address):

		self.videoStreamer.setPiAddress(pi_address)

		known_names, known_encodings = self.getAllFaceInfoFromDb()

		self.faceRecognizer.updateKnownFaces(known_names, known_encodings)

		self.videoStreamer.start()

	# consider changing name of this method
	@pyqtSlot(ndarray)
	def faceRecognizeFrame(self, cv_img):

		self.setCurrentFrame(cv_img)

		if self.performFacialRecognition:

			cv_img = self.faceRecognizer.findImageFaces(cv_img)

		self.changeFrame.emit(cv_img)

		# todo - check for unknown in names, signal observer if found

	def recognizeAndRecordCurrentFrame(self):

		print(self.currentAddFaceName)

		face_encoding = self.faceRecognizer.getImageFaceEncoding(self.currentFrame)

		print(face_encoding)

		self.currentAddFaceEncodings.append(face_encoding)

	def checkNameExistenceInDb(self, name):

		sql = "SELECT FaceName FROM faces WHERE FaceName = ?"

		db_response = self.database.executeQuery(sql, variables=[name])

		if db_response:
			return True
		else:
			return False

	def addFaceToDb(self):

		# name - str
		# encodings - list of lists
		encodings_bytes = pickle.dumps(self.currentAddFaceEncodings)

		sql = "INSERT INTO faces (FaceName, FaceEncodings) VALUES (?, ?)"

		self.database.executeNonQuery(sql, variables=[self.currentAddFaceName, encodings_bytes])

		self.currentAddFaceEncodings = list()
		self.currentAddFaceName = None

		print("Face added!")

	def deleteFaceFromDb(self, name):

		sql = "DELETE FROM faces WHERE FaceName = ?"

		self.database.executeNonQuery(sql, variables=[name])

	def deleteAllFacesFromDb(self):

		self.database.wipeDatabase()

		create_sql = "CREATE TABLE IF NOT EXISTS faces (FaceName TEXT PRIMARY KEY," \
					 "FaceEncodings BLOB NOT NULL)"

		self.database.createDatabase(create_sql)



