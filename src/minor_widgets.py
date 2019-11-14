# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont


class ConnectToPiWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel("Connect to Raspberry Pi")

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        self.ipAddressInput = QLineEdit()
        self.ipAddressInput.setPlaceholderText("IP Address")

        self.submitButton = QPushButton("Connect!")

        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.ipAddressInput)
        self.mainLayout.addWidget(self.submitButton)
