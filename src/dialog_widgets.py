# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from PyQt5.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal


class GetFaceNameDialog(QDialog):
    """
    GetFaceNameDialog class - derived from QDialog

    INPUTS:  None.
    OUTPUTS: None.

    Notes: This object is responsible for getting the names of faces to add and delete.
    """

    def __init__(self, label_text, button_text):
        """Initialize the GetFaceNameDialog

        Inputs:  label_text - string, button_text - string
        Outputs: Creates an instance of the GetFaceNameDialog

        """

        # init the QDialog
        super().__init__()

        # member to hold the user inputted name
        self.name = None

        # VBoxLayout to hold each widget
        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel(label_text)

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        # set bold font for the label
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        # line edit for user's to type a name into
        self.nameInput = QLineEdit()
        # example ghost text on the line edit
        self.nameInput.setPlaceholderText("John Doe")

        # submit button to capture text from the line edit
        self.submitButton = QPushButton(button_text)
        # connect the submitButton's clicked signal to the validateOnSubmit method
        self.submitButton.clicked.connect(self.validateOnSubmit)

        # add widgets to the layout
        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.nameInput)
        self.mainLayout.addWidget(self.submitButton)

    def validateOnSubmit(self):
        """
        GetFaceNameDialog - validateOnSubmit
        :return:

        NOTES: makes sure inputted name is not empty and then sets the dialog to Accepted
        """

        # get text from the line edit
        new_name = self.nameInput.text()

        # make sure something was typed in
        if new_name != "":

            # set name member
            self.name = new_name

            # accept the dialog - makes it disappear
            self.accept()

        else:
            # tell the user they need to enter a name
            QMessageBox.information(self, "No Name Entered", "You must specify a name.")


class CaptureFaceImagesDialog(QDialog):
    """
    CaptureFaceImagesDialog class - derived from QDialog

    INPUTS:  None.
    OUTPUTS: None.

    Notes: This object is responsible for telling the AppEngine to capture face data from the current frame.
    """

    # Signal to tell the AppEngine to capture face data from the current frame
    capture = pyqtSignal()

    def __init__(self):
        """Initialize the CaptureFaceImagesDialog

        Inputs:  None
        Outputs: Creates an instance of the CaptureFaceImagesDialog
        """

        # init the QDialog
        super().__init__()

        # variable representing the number of frames that have been captured
        self.numCaptured = 0

        # VBoxLayout to hold widgets
        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel("Capture Images for the New Face")

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        # set bold font for the label
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        # push button to Capture frames
        self.captureButton = QPushButton("Capture")
        # connect the captureButton's clicked signal to the captureImage method
        self.captureButton.clicked.connect(self.captureImage)

        # push button to quit the dialog after desired amount of frames have been captured
        self.submitButton = QPushButton("Done")
        # connect the submitButton's clicked method to the validateOnSubmit method
        self.submitButton.clicked.connect(self.validateOnSubmit)

        # add widgets to the layout
        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.captureButton)
        self.mainLayout.addWidget(self.submitButton)

    def captureImage(self):
        """
        CaptureFaceImagesDialog - captureImage
        :return:

        NOTES: increments numCaptured and emits the capture signal which tells the AppEngine to gather face data from
               the current frame.
        """

        self.numCaptured += 1

        self.capture.emit()

    def validateOnSubmit(self):
        """
        CaptureFaceImagesDialog - validateOnSubmit
        :return:

        NOTES: ensures enough frames have been captured and then accepts the dialog.
        """

        if self.numCaptured >= 5:

            # reset num captured so that it works properly the next time a face is added
            self.numCaptured = 0

            self.accept()

        else:
            # tell the user they need to capture more images
            QMessageBox.information(self, "Not Enough Images Captured", "You must capture at least 5 images.")


class AddSubscriberDialog(QDialog):
    """
    AddSubscriberDialog class - derived from QDialog

    INPUTS:  None.
    OUTPUTS: None.

    Notes: This object is responsible for getting the phone number of a new subscriber.
    """

    def __init__(self):
        """Initialize the AddSubscriberDialog

        Inputs:  None
        Outputs: Creates an instance of the AddSubscriberDialog
        """

        # init the QDialog
        super().__init__()

        # member to hold the inputted phone number
        self.number = None

        # VBoxLayout to hold widgets
        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel("Subscribe to Alerts")

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        # set bold font for the label
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        # line edit for user input
        self.numberInput = QLineEdit()
        # example ghost text
        self.numberInput.setPlaceholderText("+13031239876")

        # submit button for when the user is finished typing in a phone number
        self.submitButton = QPushButton("Add Number")
        # connect the clicked signal of the submitButton to the validateOnSubmit method
        self.submitButton.clicked.connect(self.validateOnSubmit)

        # add widgets the the layout
        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.numberInput)
        self.mainLayout.addWidget(self.submitButton)

    def validateOnSubmit(self):
        """
        AddSubscriberDialog - validateOnSubmit
        :return:

        NOTES: ensures phone number format is valid and then accepts the dialog.
        """

        # get text from the line edit
        new_number = self.numberInput.text()

        # check that input is valid
        if len(new_number) == 12:
            if new_number[0] == '+' and new_number[1] == '1':

                # if number is valid, accept the dialog
                try:
                    int(new_number[2:])
                    self.number = new_number
                    self.accept()
                    return
                except ValueError:
                    pass

        # notify the user of the error
        QMessageBox.information(self, "Incorrect phone number format", "Acceptable input is of the form: <+19879879876>.\nThe number '{}' will not recieve alerts.".format(new_number))