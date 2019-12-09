# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from PyQt5.QtCore import QObject, pyqtSignal
from numpy import ndarray
import face_recognition
import cv2


class FaceRecognizer(QObject):

    # SIGNALS GO HERE
    # newLabeledImg = pyqtSignal(ndarray)

    def __init__(self):

        super().__init__()

        # TODO - populate faces from db
        self.face_dict = None

    def updateKnownFaces(self, new_face_dict):

        self.face_dict = new_face_dict

    def findImageFaces(self, cv_img):

        # SOURCE/CREDIT: https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

        # cv_img = cv2.flip(cv_img, 0)

        # change pix format from BGR to RGB
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        # face detection model to use: either `hog` or `cnn`
        boxes = face_recognition.face_locations(rgb, model='hog')

        # encodings = face_recognition.face_encodings(rgb, boxes)

        for (top, right, bottom, left) in boxes:
            # draw the predicted face name on the image
            cv2.rectangle(cv_img, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(cv_img, "UNKNOWN", (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # self.newLabeledImg.emit(cv_img)
        return cv_img

    def getImageFaceEncoding(self, cv_img):

        # change pix format from BGR to RGB
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        # face detection model to use: either `hog` or `cnn`
        boxes = face_recognition.face_locations(rgb, model='hog')

        encoding = face_recognition.face_encodings(rgb, boxes)

        return encoding





