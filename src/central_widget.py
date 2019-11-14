# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from minor_widgets import ConnectToPiWidget


class CentralWidget(QWidget):
    """
    CentralWidget class - derived from QWidget

    INPUTS:  None.

    """

    def __init__(self):
        """
        Initialize the central widget

        Inputs:  None.
        """

        super().__init__()

        # Placeholder for future object
        self.engine = None

        # -------------------------------
        # Layouts and widgets go here
        # -------------------------------

        self.mainLayout = QVBoxLayout(self)

        self.connectWidget = ConnectToPiWidget()

        self.mainLayout.addWidget(self.connectWidget)
