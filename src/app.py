# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


class App(QApplication):
	"""
	App class - derived from QApplication

	INPUTS:  None, does not take cmd args.
	OUTPUTS: Creates an instance of the MainWindow and shows it.

	Notes: A single instance of the App class is created by the main function
		   when the program begins execution.
	"""

	def __init__(self):
		"""Initialize the application

		Input:  None
		Output: Sets application name and creates the main window.

		"""
		# Initialize the parent widget
		super().__init__([])

		# Set the application name
		self.setApplicationName("Facial Recognition App")

		# Create the main    window
		self.mainWindow = MainWindow()


		# Show the main window
		# Note: show() is non-blocking, exec() is blocking
		self.mainWindow.show()


def main():
	"""
	main - main function of app.py

	INPUTS:  None. Does not take cmd args.
	OUTPUTS: Creates instance of App class and executes it.
	"""
	app = App()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
