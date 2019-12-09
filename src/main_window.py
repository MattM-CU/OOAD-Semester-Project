# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QMessageBox
from central_widget import CentralWidget
from dialog_widgets import GetFaceNameDialog, CaptureFaceImagesDialog, AddSubscriberDialog


class MainWindow(QMainWindow):
	"""
	MainWindow class - derived from QMainWindow

	INPUTS:  None.
	OUTPUTS: Holds the menu bar for the GUI as well as the CentralWidget.

	"""
	def __init__(self):
		"""Initialize the main window.

		   Input:  None
		   Output: Titles the window, creates instance of CentralWidget,
		   		   sets up the menu bar menus and their actions.
		"""

		# Initialize the parent widget
		super().__init__()

		# Name the window
		self.setWindowTitle("Facial Recognition App")

		# Create a main widget object (the central widget)
		self.mainWidget = CentralWidget()

		# create the menu bar and its two menus: file and edit
		self.menuBar = QMenuBar()
		self.file = self.menuBar.addMenu("File")
		self.edit = self.menuBar.addMenu("Edit")

		# Add action for File->Exit
		self.file_exit = self.file.addAction("Exit")
		self.file_exit.triggered.connect(self.closeApp)

		# create menu bar action for toggling facial recognition
		self.file_recognize_faces = QAction("Facial Recognition", self.menuBar, checkable=True)
		self.file.addAction(self.file_recognize_faces)
		self.file_recognize_faces.triggered.connect(self.changeFacialRecognitionState)

		# Add actions for Edit

		# create menu bar action for subscribing to SMS alerts
		self.edit_subscribeAlerts = self.edit.addAction("Subscribe to Alerts...")
		self.edit_subscribeAlerts.triggered.connect(self.subscribeToAlerts)

		# create menu bar action for adding a new face
		self.edit_addFace = self.edit.addAction("Add a New Face...")
		self.edit_addFace.triggered.connect(self.addNewFace)

		# create dialog widget to allow users to capturing face images (for adding a new face)
		self.captureFaceImagesDialog = CaptureFaceImagesDialog()
		# connect the dialog's capture signal ot the Engine's recognizeAndRecordCurrentFrame method
		self.captureFaceImagesDialog.capture.connect(self.mainWidget.engine.recognizeAndRecordCurrentFrame)

		# menu bar action for deleting a specific face
		self.edit_deleteFace = self.edit.addAction("Delete a Face...")
		self.edit_deleteFace.triggered.connect(self.deleteFace)

		# menu bar action for deleting all known faces from the application
		self.edit_deleteAllFaces = self.edit.addAction("Delete All Faces")
		self.edit_deleteAllFaces.triggered.connect(self.deleteAllFaces)

		# set the menu bar
		self.setMenuBar(self.menuBar)

		#  Set the main widget object as the central widget of the main window
		self.setCentralWidget(self.mainWidget)

	def closeApp(self):
		"""
		MainWindow - closeApp

		INPUTS:  None.
		OUTPUTS: Closes the app, same as clicking the x.
		"""
		self.close()

	def changeFacialRecognitionState(self):
		"""
		MainWindow - changeFacialRecognitionState
		:return:

		NOTES: depending on whether or not the File->Facial Recognition is toggled on or off, set the Engine's
			   facial recognition state boolean.
		"""

		# determine if option is toggled on or off
		if self.file_recognize_faces.isChecked():
			self.mainWidget.engine.setFacialRecognitionState(True)
		else:
			self.mainWidget.engine.setFacialRecognitionState(False)

	def subscribeToAlerts(self):
		"""
		MainWindow - subscribeToAlerts
		:return:

		NOTES: creates the AddSubscriberDialog, waits for acceptance and then call's the Engine's addObserver method.
		"""

		# create the dialog
		getPhoneNumberDialog = AddSubscriberDialog()

		# exec the dialog and wait for acceptance
		if (getPhoneNumberDialog.exec() == getPhoneNumberDialog.Accepted):

			# get the inputted phone number once accepted
			added_phone_number = getPhoneNumberDialog.number

			# Notify the user of success
			QMessageBox.information(self, "Number Added", "Alerts will now be sent to {}".format(added_phone_number))

			# Add number to the AlertObserver (called from engine)
			self.mainWidget.engine.addObserver(added_phone_number)

	def addNewFace(self):
		"""
		MainWindow - addNewFace
		:return:

		NOTES: This method creates a dialog prompting the user to enter a new face name, gets the name, and then creates
			   another dialog allowing the user to capture images of the new face to add.
		"""

		# make sure application is connected to the Pi so images can be captured
		if not self.mainWidget.isConnectedToPi():

			# notify the user that they must connect to the Pi first
			QMessageBox.information(self, "Not Connected To Pi", "You must connect to the Pi before adding a new face.")

		else:
			# create dialog for getting new face name
			getNameDialog = GetFaceNameDialog("Enter a Name for the New Face", "Add")

			# exec the dialog and wait for acceptance
			if (getNameDialog.exec() == getNameDialog.Accepted):

				# get the inputted name from the dialog
				new_face_name = getNameDialog.name

				# make sure the name doesn't already exist in the database
				if self.mainWidget.engine.checkNameExistenceInDb(new_face_name):

					# warn the user that the given name already exists
					QMessageBox.warning(self, "Name Already Exists", "This face name is already present in the database.")

				else:
					# disable facial recognition so the user can see the face better when capturing images
					self.file_recognize_faces.setChecked(False)
					self.mainWidget.engine.setFacialRecognitionState(False)

					self.file_recognize_faces.setEnabled(False)

					# set the Engine's member for the name of the current face to add
					self.mainWidget.engine.setCurrentAddFaceName(new_face_name)

					# logic for capturing images

					# create the dialog prompting users to take pictures - clicking capture will signal the Engine
					if (self.captureFaceImagesDialog.exec() == self.captureFaceImagesDialog.Accepted):

						# print("Done capturing images.")

						# after dialog is accepted, tell the Engine to add the new face to the database
						self.mainWidget.engine.addFaceToDb()

						# re-enable the facial recognition toggle
						self.file_recognize_faces.setEnabled(True)

					# if dialog is rejected, reset Engine's add face data and re-enable the facial recognition toggle
					else:

						self.mainWidget.engine.resetCurrentAddFaceData()

						self.file_recognize_faces.setEnabled(True)

	def deleteFace(self):
		"""
		MainWidget - deleteFace
		:return:

		NOTES: creates a dialog prompting the user to enter a name for the face to delete, calls the Engine's method
			   to delete a specific face (if it exists in the database).
		"""

		# create dialog to get the name of the face to delete
		getNameDialog = GetFaceNameDialog("Enter the Name of the Face to Delete", "Delete")

		# wait for the dialog to be accepted
		if (getNameDialog.exec() == getNameDialog.Accepted):

			# get the name from the dialog
			delete_face_name = getNameDialog.name

			# make sure the name actually exists in the DB before attempting to delete it
			if not self.mainWidget.engine.checkNameExistenceInDb(delete_face_name):

				QMessageBox.warning(self, "Name Does Not Exist", "This face name does not exist in the database.")

			else:
				# delete the face and let the user know it was successful
				self.mainWidget.engine.deleteFaceFromDb(delete_face_name)

				QMessageBox.information(self, "Face Deleted", "The specified face has been successfully deleted.")

	def deleteAllFaces(self):
		"""
		MainWidget - deleteAllFaces
		:return:

		NOTES: prompts user for validation and then clears all face data from the database if they say yes.
		"""

		# create the validation message box
		validation = QMessageBox()

		# make the user confirm that they want to wipe the database
		ret = validation.question(self, '', "Are you sure you want to wipe the database?", validation.Yes | validation.No)

		# delete all faces from the database if user said yes
		if ret == validation.Yes:
			# wipe the db
			self.mainWidget.engine.deleteAllFacesFromDb()
