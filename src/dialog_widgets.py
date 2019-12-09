# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal


class GetFaceNameDialog(QDialog):

    # newFaceName = pyqtSignal(str)

    def __init__(self, label_text, button_text):

        super().__init__()

        self.name = None

        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel(label_text)

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        # set bold font for the label
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        self.nameInput = QLineEdit()

        self.nameInput.setPlaceholderText("John Doe")

        self.submitButton = QPushButton(button_text)
        self.submitButton.clicked.connect(self.validateOnSubmit)

        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.nameInput)
        self.mainLayout.addWidget(self.submitButton)

    def validateOnSubmit(self):

        new_name = self.nameInput.text()

        if new_name != "":

            # self.newFaceName.emit(new_name)
            self.name = new_name

            self.accept()

        else:

            QMessageBox.information(self, "No Name Entered", "You must specify a name.")


class CaptureFaceImagesDialog(QDialog):

    # Signal here
    capture = pyqtSignal()

    # doneCapturing = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.numCaptured = 0

        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel("Capture Images for the New Face")

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        # set bold font for the label
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        self.captureButton = QPushButton("Capture")
        self.captureButton.clicked.connect(self.captureImage)

        self.submitButton = QPushButton("Done")
        self.submitButton.clicked.connect(self.validateOnSubmit)

        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.captureButton)
        self.mainLayout.addWidget(self.submitButton)

    def captureImage(self):

        self.numCaptured += 1

        self.capture.emit()

    def validateOnSubmit(self):

        if self.numCaptured >= 5:

            # self.doneCapturing.emit()
            self.numCaptured = 0

            self.accept()

        else:

            QMessageBox.information(self, "Not Enough Images Captured", "You must capture at least 5 images.")




