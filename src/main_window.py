# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QMainWindow, QMenuBar, QAction, QMessageBox, QDialog
from central_widget import CentralWidget
from dialog_widgets import GetFaceNameDialog, CaptureFaceImagesDialog


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

		self.file_recognize_faces = QAction("Facial Recognition", self.menuBar, checkable=True)
		self.file.addAction(self.file_recognize_faces)
		self.file_recognize_faces.triggered.connect(self.changeFacialRecognitionState)

		# Add actions for Edit
		self.edit_subscribeAlerts = self.edit.addAction("Subscribe to Alerts...")
		self.edit_subscribeAlerts.triggered.connect(self.subscribeToAlerts)

		self.edit_addFace = self.edit.addAction("Add a New Face...")
		self.edit_addFace.triggered.connect(self.addNewFace)

		self.captureFaceImagesDialog = CaptureFaceImagesDialog()
		self.captureFaceImagesDialog.capture.connect(self.mainWidget.engine.recognizeAndRecordCurrentFrame)

		self.edit_deleteFace = self.edit.addAction("Delete a Face...")
		self.edit_deleteFace.triggered.connect(self.deleteFace)

		self.edit_deleteAllFaces = self.edit.addAction("Delete All Faces")
		self.edit_deleteAllFaces.triggered.connect(self.deleteAllFaces)

		# set the menu bar
		self.setMenuBar(self.menuBar)

		#  Set the main widget object as the central widget of the main window
		self.setCentralWidget(self.mainWidget)

	def closeApp(self):
		"""
		closeApp - method of MainWindow

		INPUTS:  None.
		OUTPUTS: Closes the app, same as clicking the x.
		"""
		self.close()

	def changeFacialRecognitionState(self):

		if self.file_recognize_faces.isChecked():
			self.mainWidget.engine.setFacialRecognitionState(True)
		else:
			self.mainWidget.engine.setFacialRecognitionState(False)

	def subscribeToAlerts(self):
		pass

	def addNewFace(self):

		# if not self.mainWidget.isConnectedToPi():
		#
		# 	QMessageBox.information(self, "Not Connected To Pi", "You must connect to the Pi before adding a new face.")

		getNameDialog = GetFaceNameDialog("Enter a Name for the New Face", "Add")

		if (getNameDialog.exec() == getNameDialog.Accepted):

			new_face_name = getNameDialog.name

			if self.mainWidget.engine.checkNameExistenceInDb(new_face_name):

				QMessageBox.warning(self, "Name Already Exists", "This face name is already present in the database.")

			else:
				self.file_recognize_faces.setChecked(False)
				self.mainWidget.engine.setFacialRecognitionState(False)

				self.file_recognize_faces.setEnabled(False)

				self.mainWidget.engine.setCurrentAddFaceName(new_face_name)

				# logic for capturing images
				if (self.captureFaceImagesDialog.exec() == self.captureFaceImagesDialog.Accepted):

					print("Done capturing images.")

					# todo - make sure CurrentAddFaceName is set to None somewhere
					self.mainWidget.engine.addFaceToDb()

					self.file_recognize_faces.setEnabled(True)
				# todo

	def deleteFace(self):

		getNameDialog = GetFaceNameDialog("Enter the Name of the Face to Delete", "Delete")

		if (getNameDialog.exec() == getNameDialog.Accepted):

			delete_face_name = getNameDialog.name

			if not self.mainWidget.engine.checkNameExistenceInDb(delete_face_name):

				QMessageBox.warning(self, "Name Does Not Exist", "This face name does not exist in the database.")

			else:
				self.mainWidget.engine.deleteFaceFromDb(delete_face_name)

				QMessageBox.information(self, "Face Deleted", "The specified face has been successfully deleted.")

	def deleteAllFaces(self):

		validation = QMessageBox()

		ret = validation.question(self, '', "Are you sure you want to wipe the database?", validation.Yes | validation.No)

		if ret == validation.Yes:
			# wipe the db
			self.mainWidget.engine.deleteAllFacesFromDb()

