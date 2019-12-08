# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QImage, QPixmap, QTransform
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from video_streamer import VideoStreamer
import re


class ConnectToPiWidget(QWidget):

    connectSignal = pyqtSignal(str)

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
        self.submitButton.clicked.connect(self.connectClicked)

        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.ipAddressInput)
        self.mainLayout.addWidget(self.submitButton)

    def connectClicked(self):

        pi_address = self.ipAddressInput.text()

        if not pi_address == "":

            # format_check = re.search(TODO)

            self.connectSignal.emit(pi_address)



# https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv
class VideoWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.label = QLabel(self)

        # self.video_streamer = VideoStreamer()
        # self.video_streamer.changeFrame.connect(self.setImage)

    def videoSetup(self):

        self.label.resize(640, 480)

        # self.video_streamer.setPiAddress(pi_address)

        # self.video_streamer.start()

        self.setFixedSize(640, 480)

    # @pyqtSlot(QImage)
    def setImage(self, image):

        # rotate180 = QTransform().rotate(180)
        #
        # # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
        height, width, channel = image.shape
        bytesPerLine = 3 * width

        qtImage = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()#.transformed(rotate180)

        self.label.setPixmap(QPixmap.fromImage(qtImage))

    # def setupImgDisplay(self):
    #
    #     # todo, make sure pi_address is not none
    #
    #     self.label.resize(640, 480)
    #
    #     video_streamer = VideoStreamer(self.pi_address)
    #
    #     video_streamer.changeFrame.connect(self.setImage)
    #
    #     video_streamer.start()


#
# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         [...]
#         self.initUI()
#
#     @pyqtSlot(QImage)
#     def setImage(self, image):
#         self.label.setPixmap(QPixmap.fromImage(image))
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.resize(1800, 1200)
#         # create a label
#         self.label = QLabel(self)
#         self.label.move(280, 120)
#         self.label.resize(640, 480)
#         th = Thread(self)
#         th.changePixmap.connect(self.setImage)
#         th.start()
