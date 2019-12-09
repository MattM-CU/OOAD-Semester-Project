# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedLayout
from PyQt5.QtCore import pyqtSlot
from numpy import ndarray
from minor_widgets import ConnectToPiWidget, VideoWidget
from app_engine import AppEngine
import time


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
        self.engine = AppEngine()
        self.engine.changeFrame.connect(self.setVideoWidgetFrame)

        # -------------------------------
        # Layouts and widgets go here
        # -------------------------------

        # self.mainLayout = QVBoxLayout(self)
        self.mainLayout = QStackedLayout(self)

        self.connectWidget = ConnectToPiWidget()
        self.connectWidget.connectSignal.connect(self.initVideo)

        self.connectedToPi = False

        self.mainLayout.addWidget(self.connectWidget)

        self.videoWidget = VideoWidget()
        self.mainLayout.addWidget(self.videoWidget)

        self.mainLayout.setCurrentIndex(0)

    def isConnectedToPi(self):

        return self.connectedToPi

    @pyqtSlot(str)
    def initVideo(self, pi_address):

        self.videoWidget.videoSetup()

        self.engine.connectToPi(pi_address)

        self.connectedToPi = True

        self.mainLayout.setCurrentIndex(1)

    @pyqtSlot(ndarray)
    def setVideoWidgetFrame(self, overlayed_img):

        self.videoWidget.setImage(overlayed_img)
