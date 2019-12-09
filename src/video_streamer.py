# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QTransform
# import socket
import subprocess
from numpy import ndarray
import cv2

# https://picamera.readthedocs.io/en/release-1.10/recipes1.html
class VideoStreamer(QThread):

    # changeFrame = pyqtSignal(QImage)
    newPiFrame = pyqtSignal(ndarray)

    def __init__(self):
        super().__init__()

        self.pi_address = None

    def setPiAddress(self, pi_address):

        self.pi_address = pi_address

    def run(self):

        pi_stream_addr = 'tcp://' + self.pi_address + ':8001'

        # https://raspberrypi.stackexchange.com/questions/100150/read-ip-camera-stream-video-on-python-using-opencv3
        cap = cv2.VideoCapture(pi_stream_addr)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Frame not read properly :(")
                # time.sleep(0.1)
                break

            # rotate180 = QTransform().rotate(180)

            # https://stackoverflow.com/questions/34232632/convert-python-opencv-image-numpy-array-to-pyqt-qpixmap-image
            # height, width, channel = frame.shape
            # bytesPerLine = 3 * width
            #
            # qtImageFrame = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped().transformed(rotate180)

            # self.changeFrame.emit(qtImageFrame)

            frame = cv2.flip(frame, 0)

            self.newPiFrame.emit(frame)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # When everything's done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        # todo - maybe send a signal here to switch back to the connect widget


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

    # def run(self):
    #
    #     server_socket = socket.socket()
    #     # server_socket.connect(('192.168.0.98', 8001))
    #     server_socket.connect((self.pi_address, 8001))
    #
    #     connection = server_socket.makefile('rb')
    #
    #     while True:
    #         # Repeatedly read 1k of data from the connection and write it to
    #         # the media player's stdin
    #         data = connection.read(1024)
    #
    #         if not data:
    #             break
    #
    #         #player.stdin.write(data)
    #         # qtImageFrame = QImage(data, 640, 480, QImage.Format_RGB888)
    #         qtImageFrame = QImage()
    #         success = qtImageFrame.loadFromData(data)
    #
    #         if success:
    #             self.changeFrame.emit(qtImageFrame)
    #         else:
    #             # maybe do something here?
    #             print("Could not make QImage")
    #
    #     connection.close()
    #     server_socket.close()
