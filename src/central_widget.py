# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QWidget, QStackedLayout
from PyQt5.QtCore import pyqtSlot
from numpy import ndarray
from minor_widgets import ConnectToPiWidget, VideoWidget
from app_engine import AppEngine


class CentralWidget(QWidget):
    """
    CentralWidget class - derived from QWidget

    INPUTS:  None.
    OUTPUTS: None

    NOTES: The CentralWidget holds the AppEngine, ConnectToPiWidget and the VideoWidget
    """

    def __init__(self):
        """Initialize the central widget

        Inputs:  None.
        Outputs: Creates an instance of the CentralWidget
        """

        # initialize QWidget
        super().__init__()

        # create the AppEngine object which facilitates communication b/t major system components
        self.engine = AppEngine()
        # connect the AppEngine's changeFrame signal to the setVideoWidgetFrame method
        self.engine.changeFrame.connect(self.setVideoWidgetFrame)

        # -------------------------------
        # Layouts and widgets
        # -------------------------------

        # stacked layout to switch b/t ConnectToPiWidget and VideoWidget
        self.mainLayout = QStackedLayout(self)

        # create the ConnectToPiWidget
        self.connectWidget = ConnectToPiWidget()
        # connect the ConnectWidget's signal to the initVideo method
        self.connectWidget.connectSignal.connect(self.initVideo)

        # bool to determine if the Pi has been connected
        self.connectedToPi = False

        # create the VideoWidget
        self.videoWidget = VideoWidget()

        # add each widget to the layout
        self.mainLayout.addWidget(self.connectWidget)
        self.mainLayout.addWidget(self.videoWidget)

        # display ConnectWidget by default
        self.mainLayout.setCurrentIndex(0)

    def isConnectedToPi(self):
        """
        CentralWidget - isConnectedToPi
        :return: bool - true if the Pi is connected
        """

        return self.connectedToPi

    @pyqtSlot(str)
    def initVideo(self, pi_address):
        """
        CentralWidget - initVideo
        :param pi_address: str - the IP (or hostname) of the RaspberryPi
        :return:

        NOTES: This method is a slot which gets called when the ConnectWidget emits its signal
        """

        # set up the VideoWidget so it can display frames
        self.videoWidget.videoSetup()

        # make engine connect to the Pi - this will capture the video stream
        self.engine.connectToPi(pi_address)

        self.connectedToPi = True

        # set the current displayed widget to the VideoWidget
        self.mainLayout.setCurrentIndex(1)

    @pyqtSlot(ndarray)
    def setVideoWidgetFrame(self, overlayed_img):
        """
        CentralWidget - setVideoWidgetFrame
        :param overlayed_img: numpy.ndarray
        :return:

        NOTES: This method is a slot which gets called when the AppEngine emits its changeFrame signal. This changes
               the VideoWidget's current frame and displays it.
        """

        # set the VideoWidget's current image
        self.videoWidget.setImage(overlayed_img)
