# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QMainWindow, QMenuBar
from central_widget import CentralWidget


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

		# Add actions for Edit
		self.edit_subscribeAlerts = self.edit.addAction("Subscribe to Alerts...")
		self.edit_subscribeAlerts.triggered.connect(self.subscribeToAlerts)

		self.edit_addFace = self.edit.addAction("Add a New Face...")
		self.edit_addFace.triggered.connect(self.addNewFace)

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

	def subscribeToAlerts(self):
		pass

	def addNewFace(self):
		pass

	def deleteFace(self):
		pass

	def deleteAllFaces(self):
		pass
