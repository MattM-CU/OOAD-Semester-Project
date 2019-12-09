# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from numpy import ndarray
from db_connect import Database
from video_streamer import VideoStreamer
from face_recognizer import FaceRecognizer
from alert_observer import AlertObserver
import pickle


class AppEngine(QObject):
	"""
	AppEngine class - derived from QObject

	INPUTS:  None
	OUTPUTS: None

	Notes: Mediator object for the application, facilitates communication b/t other objects
	"""

	# signal to update the VideoWidget's current frame
	changeFrame = pyqtSignal(ndarray)

	def __init__(self):
		"""Initialize the AppEngine

		Input:  None
		Output: Creates an instance of the AppEngine.
		"""

		# init QObject
		super().__init__()

		# create an instance of the database
		self.database = Database('../data/face_data.db')

		# ensure appropriate table is created
		create_sql = "CREATE TABLE IF NOT EXISTS faces (FaceName TEXT PRIMARY KEY," \
					 "FaceEncodings BLOB NOT NULL)"
		self.database.createDatabase(create_sql)

		# create an instance of the VideoStreamer
		self.videoStreamer = VideoStreamer()
		# connect the VideoStreamer's newPiFrame signal to the processNewFrame method
		self.videoStreamer.newPiFrame.connect(self.processNewFrame)

		# create an instance of the FaceRecognizer
		self.faceRecognizer = FaceRecognizer()

		# bool which determines if facial recognition is performed on each incoming frame from the Pi
		self.performFacialRecognition = False

		# current frame sent from the Pi, used for adding a new face
		self.currentFrame = None

		# current face name and encodings, used for adding a new face
		self.currentAddFaceName = None
		self.currentAddFaceEncodings = list()

		# create an instance of the AlertObserver
		self.alertObserver = AlertObserver()

		# bool determines if an alert has already been sent (only one is sent per application run)
		self.alertSent = False

	def setCurrentFrame(self, frame):
		"""
		AppEngine - setCurrentFrame
		:param frame: numpy.ndarray - represents a cv2 image
		:return:

		NOTES: set the AppEngine's current frame member
		"""

		self.currentFrame = frame

	def setCurrentAddFaceName(self, name):
		"""
		AppEngine - setCurrentAddFaceName
		:param name: str - the name to set
		:return:

		NOTES: set the AppEngine's current add face name member
		"""

		self.currentAddFaceName = name

	def resetCurrentAddFaceData(self):
		"""
		AppEngine - resetCurrentAddFaceData
		:return:

		NOTES: resets the members holding info for a new face to be added.
		"""

		self.currentAddFaceName = None
		self.currentAddFaceEncodings = list()

	def setFacialRecognitionState(self, state_bool):
		"""
		AppEngine - setFacialRecognitionState
		:param state_bool: bool
		:return:

		NOTES: sets the AppEngine's facial recognition state (determines if facial recognition will be performed on
			   each frame.
		"""

		self.performFacialRecognition = state_bool

	def getAllFaceInfoFromDb(self):
		"""
		AppEngine - getAllFaceInfoFromDb
		:return: face_names - list<str>, face_encodings - list<array>

		NOTES: gets all face names and their corresponding encodings from the database and returns them.
		"""

		# empty lists to hold names and encodings
		face_names = list()
		face_encodings = list()

		# sql to get everything from the faces table
		sql = "SELECT * FROM faces"

		results = self.database.executeQuery(sql, variables=[])

		# iterate over results, collect data into the lists
		for row in results:

			# load pickled data - returns list of arrays
			# https://stackoverflow.com/questions/52890916/python3-unpickle-a-string-representation-of-bytes-object
			current_face_encodings = pickle.loads(eval(row['FaceEncodings']))

			# make sure length of names is the same as encodings - necessary for recognizing named faces
			face_names = face_names + ([row['FaceName']] * len(current_face_encodings))

			face_encodings = face_encodings + current_face_encodings

		# face encodings list needs to be flattened (b/c each sublist is only length 1)
		return face_names, [encoding[0] for encoding in face_encodings]

	def connectToPi(self, pi_address):
		"""
		AppEngine - connectToPi
		:param pi_address: str - the ip address (or hostname) of the RaspberryPi
		:return:

		NOTES: sets up the VideoStreamer to connect to the Pi, update FaceRecognizer data, and then starts the
			   VideoStreamer's thread.
		"""

		# set the address of the VideoStreamer
		self.videoStreamer.setPiAddress(pi_address)

		# update known face data
		self.updateFaceRecognizerData()

		# start VideoStreamer thread
		self.videoStreamer.start()

	def updateFaceRecognizerData(self):
		"""
		AppEngine - updateFaceRecognizerData
		:return:

		NOTES: gets all face info from the database then updates that data in the FaceRecognizer.
		"""

		# get face data from the database
		known_names, known_encodings = self.getAllFaceInfoFromDb()

		# set FaceRecognizer data using the new info
		self.faceRecognizer.updateKnownFaces(known_names, known_encodings)

	@pyqtSlot(ndarray)
	def processNewFrame(self, cv_img):
		"""
		AppEngine - processNewFrame
		:param cv_img: numpy.ndarray
		:return:

		NOTES: updates AppEngine's current frame, performs facial recognition if needed, alerts observers if unknown
			   face is found, sends signal to update the VideoWidget's frame.
		"""

		# update the current frame
		self.setCurrentFrame(cv_img)

		# check if facial recognition needs to be performed
		if self.performFacialRecognition:

			# get box-overlayed image and the names of detected faces in the image
			cv_img, names = self.faceRecognizer.findImageFaces(cv_img)

			# check if an alert has already been sent, if not, check if an unknown face was found in the image
			if not self.alertSent:
				if "Unknown" in names:

					# try-except catches errors resulting from unregistered phone numbers
					try:
						# send SMS messages to each of the observers
						self.alertObserver.alertObservers()
					except Exception:
						pass

					self.alertSent = True

		# emit signal to change the VideoWidget's displayed frame (may be overlaid with face boxes or not)
		self.changeFrame.emit(cv_img)

	def recognizeAndRecordCurrentFrame(self):
		"""
		AppEngine - recognizeAndRecordCurrentFrame
		:return:

		NOTES: only called when user clicks 'Capture' in the MainWindow's CaptureFaceImagesDialog. This method
			   will get the face encoding from the immage and update the AppEngine's list of encodings.
		"""

		# get face encoding data from the current frame
		face_encoding = self.faceRecognizer.getImageFaceEncoding(self.currentFrame)

		# update list of encodings for the new face to be added
		self.currentAddFaceEncodings.append(face_encoding)

	def checkNameExistenceInDb(self, name):
		"""
		AppEngine - checkNameExistenceInDb
		:param name: str
		:return: bool - true if name already exists in the database

		NOTES: checks if the specified name is already present in the database.
		"""

		# sql to check if the name is in the database
		sql = "SELECT FaceName FROM faces WHERE FaceName = ?"

		# execute the query
		db_response = self.database.executeQuery(sql, variables=[name])

		# response will be an empty list if name does not exist in the database
		if db_response:
			return True
		else:
			return False

	def addObserver(self, observer_number):
		"""
		AppEngine - addObserver
		:param observer_number: str - phone number of the observer to add
		:return:

		NOTES: adds the new phone number to the AlertObserver's list of observers
		"""
		self.alertObserver.addObserver(observer_number)

	def addFaceToDb(self):
		"""
		AppEngine - addFaceToDb
		:return:

		NOTES: only called when the user clicks 'Done' in the MainWindow's CaptureFaceImagesDialog. This will add the
			   current face name and corresponding encodings to the database.
		"""

		# pickle the encodings (list of arrays) so that they can be saved into the database and reconstructed later
		encodings_bytes = pickle.dumps(self.currentAddFaceEncodings)

		# sql to insert face data
		sql = "INSERT INTO faces (FaceName, FaceEncodings) VALUES (?, ?)"

		self.database.executeNonQuery(sql, variables=[self.currentAddFaceName, encodings_bytes])

		# reset the AppEngine's data so that another named face can be added
		self.resetCurrentAddFaceData()

		# update the FaceRecognizer's data so that it can recognize the new face
		self.updateFaceRecognizerData()

	def deleteFaceFromDb(self, name):
		"""
		AppEngine - deleteFaceFromDb
		:param name: str
		:return:

		NOTES: deletes data from the database corresponding to the given name
		"""

		# sql to delete the specific face
		sql = "DELETE FROM faces WHERE FaceName = ?"

		self.database.executeNonQuery(sql, variables=[name])

		# update the FaceRecognizer's data since it just changed
		self.updateFaceRecognizerData()

	def deleteAllFacesFromDb(self):
		"""
		AppEngine - deleteAllFacesFromDb
		:return:

		NOTES: wipes the database and then recreates the faces table.
		"""

		# wipe the database (drops all tables)
		self.database.wipeDatabase()

		# sql to recreate the faces table since it was dropped
		create_sql = "CREATE TABLE IF NOT EXISTS faces (FaceName TEXT PRIMARY KEY," \
					 "FaceEncodings BLOB NOT NULL)"

		# recreate the faces table
		self.database.createDatabase(create_sql)

		# update the FaceRecognizer's data
		self.updateFaceRecognizerData()



