# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import pyqtSignal


class ConnectToPiWidget(QWidget):
    """
    ConnectToPiWidget class - derived from QWidget

    INPUTS:  None.
    OUTPUTS: None.

    Notes: This widget is displayed by default on application start. It allows users the enter the IP address of the
           RaspberryPi and connect to it.
    """

    # Signal telling the application to connect to the pi via it's IP address
    connectSignal = pyqtSignal(str)

    def __init__(self):
        """Initialize the ConnectToPiWidget

        Inputs:  None
        Outputs: Creates an instance of the ConnectToPiWidget
        """

        # init the parent object - QWidget
        super().__init__()

        # VBoxLayout to hold tables, line edits, button
        self.mainLayout = QVBoxLayout(self)

        # Text label that will be at the top of the form
        self.topLabel = QLabel("Connect to Raspberry Pi")

        # make a bold font and add some margin so that the label stands out
        boldFont = QFont()
        boldFont.setBold(True)
        self.topLabel.setFont(boldFont)
        self.topLabel.setMargin(15)

        # line edit for getting IP address input from the user
        self.ipAddressInput = QLineEdit()
        self.ipAddressInput.setPlaceholderText("IP Address")

        # push button allowing the user to connect to the Pi
        self.submitButton = QPushButton("Connect!")
        # connect the button's clicked signal to the connectClicked method
        self.submitButton.clicked.connect(self.connectClicked)

        # add widgets to the layout
        self.mainLayout.addWidget(self.topLabel)
        self.mainLayout.addWidget(self.ipAddressInput)
        self.mainLayout.addWidget(self.submitButton)

    def connectClicked(self):
        """
        ConnectToPiWidget - connectClicked
        :return:

        NOTES: makes sure the IP address input from the line edit is not empty and then emits the connectSignal with
               the given IP.
        """

        # get text from the line edit
        pi_address = self.ipAddressInput.text()

        # make sure the text is not empty
        if not pi_address == "":

            # could do some format checking/error handling here

            # emit the connectSignal with the provided address
            self.connectSignal.emit(pi_address)


# https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv
class VideoWidget(QWidget):
    """
    VideoWidget class - derived from QWidget

    INPUTS:  None.
    OUTPUTS: None.

    Notes: This widget is switched to when the user connects to the Pi. It simply displays the current frame, which
           may have face-box overlays if the user has toggled on the facial recognition option.
    """

    def __init__(self):
        """Initialize the VideoWidget

        Inputs:  None
        Outputs: Creates an instance of the VideoWidget
        """

        # init the parent object - QWidget
        super().__init__()

        # create a label (this will have a pixmap to display the current frame)
        self.label = QLabel(self)

    def videoSetup(self):
        """
        VideoWidget - videoSetup
        :return:

        NOTES: sets the label and window size based on the size of frames sent by the Pi.
        """

        # resize the label and widget (so that it fits the image exactly)
        self.label.resize(640, 480)

        self.setFixedSize(640, 480)

    def setImage(self, image):
        """
        VideoWidget - setImage
        :param image: numpy.ndarray (represents cv2 image)
        :return:

        NOTES: converts the cv2 image into a QImage and then a sets the label's pixmap with the QImage
        """

        # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image

        # logic to convert the cv2 image into a QImage
        height, width, channel = image.shape
        bytesPerLine = 3 * width

        qtImage = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        # set the label's pixmap to the new image
        self.label.setPixmap(QPixmap.fromImage(qtImage))
