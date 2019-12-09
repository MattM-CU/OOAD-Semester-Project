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

        self.face_names = None
        self.face_encodings = None

    def updateKnownFaces(self, face_names, face_encodings):

        self.face_names = face_names

        self.face_encodings = face_encodings

    def findImageFaces(self, cv_img):

        # SOURCE/CREDIT: https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

        # change pix format from BGR to RGB
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        # face detection model to use: either `hog` or `cnn`
        boxes = face_recognition.face_locations(rgb, model='cnn')

        encodings = face_recognition.face_encodings(rgb, boxes)

        # initialize the list of names for each face detected
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(self.face_encodings, encoding)
            name = "Unknown"

            # check to see if we have found a match
            if (True in matches):
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = self.face_names[i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number of
                # votes (note: in the event of an unlikely tie Python will
                # select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(cv_img, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(cv_img, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # for (top, right, bottom, left) in boxes:
        #     # draw the predicted face name on the image
        #     cv2.rectangle(cv_img, (left, top), (right, bottom), (0, 255, 0), 2)
        #     y = top - 15 if top - 15 > 15 else top + 15
        #     cv2.putText(cv_img, "UNKNOWN", (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # self.newLabeledImg.emit(cv_img)
        return cv_img, names

    def getImageFaceEncoding(self, cv_img):

        # change pix format from BGR to RGB
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        # face detection model to use: either `hog` or `cnn`
        boxes = face_recognition.face_locations(rgb, model='cnn')

        encoding = face_recognition.face_encodings(rgb, boxes)

        return encoding





