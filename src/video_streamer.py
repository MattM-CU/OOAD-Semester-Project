# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtCore import QThread, pyqtSignal
from numpy import ndarray
import cv2
import time


# https://picamera.readthedocs.io/en/release-1.10/recipes1.html
class VideoStreamer(QThread):
    """
    VideoStreamer class - derived from QThread

    INPUTS:  None.
    OUTPUTS: None.

    Notes: This object runs in its own thread so that it can continually read frames from the Pi's socket without
           blocking the functionality of the GUI. It emits a signal for each frame that is read.
    """

    # signal for providing the application with a new frame from the Pi
    newPiFrame = pyqtSignal(ndarray)

    def __init__(self):
        """Initialize the VideoStreamer

        Inputs:  None
        Outputs: Creates an instance of the VideoStreamer
        """

        # init the parent object - QThread
        super().__init__()

        # member to hold the address of the Pi - will be set when the user clicks 'connect' on the connect widget
        self.pi_address = None

    def setPiAddress(self, pi_address):
        """
        VideoStreamer - setPiAddress
        :param pi_address: str - the IP/hostname of the RaspberryPi
        :return:

        NOTES: simply sets the member for the Pi's address.
        """

        self.pi_address = pi_address

    def run(self):
        """
        VideoStreamer - run
        :return:

        NOTES: connects to the Pi's TCP socket using a cv2 VideoCapture object. Continually loops and pulls frames from
               the stream until the Pi stops sending them.
        """

        # tcp connection string based on the address of the Pi
        pi_stream_addr = 'tcp://' + self.pi_address + ':8001'

        # https://raspberrypi.stackexchange.com/questions/100150/read-ip-camera-stream-video-on-python-using-opencv3
        cap = cv2.VideoCapture(pi_stream_addr)

        # loop continually - read frames from the VideoCapture
        while True:

            # Capture frame-by-frame
            ret, frame = cap.read()

            # check to see if the frame was read properly
            if not ret:
                print("Frame not read properly :(")
                break

            # flip the frame (b/c the camera is always set up upside down)
            frame = cv2.flip(frame, 0)

            # emit the newPiFrame signal with the latest frame
            self.newPiFrame.emit(frame)

            # sleep based on framerate (5 from the Pi) - this makes the video display and user IO smoother
            time.sleep(0.15)

        # When everything's done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        # maybe send a signal here to switch back to the connect widget?

    # Sad legacy code... - this sorta works though, so it's being left in as a future resource for using ffmpeg
    # def run(self):
    #     ffmpegCmd = ['ffmpeg', '-y', '-i', 'tcp://' + self.pi_address + ':8001', '-vsync', '0', '-pix_fmt', 'bgr24', '-f', 'image2pipe', '-']
    #
    #     ffmpeg = subprocess.Popen(ffmpegCmd, stdout=subprocess.PIPE, bufsize=-1)
    #
    #     while True:
    #
    #         raw_image = ffmpeg.stdout.read(640 * 480 * 3)
    #         image = np.fromstring(raw_image, dtype='uint8')  # convert read bytes to np
    #         image = image.reshape((640, 480, 3))
    #
    #         # cv2.imshow('Video', image)
    #         image = cv2.imdecode(image, 1)
    #
    #         if image is None:
    #             print("hmm")
    #             # ffmpeg.stdout.flush()
    #             continue
    #         else:
    #             height, width, channel = image.shape
    #             bytesPerLine = 3 * width
    #
    #             qtImageFrame = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
    #
    #             self.changeFrame.emit(qtImageFrame)
    #
    #         # else:
    #         #     # maybe do something here?
    #         #     print("Could not make QImage")
