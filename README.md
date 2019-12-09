Matthew Menten

Eli Jacobshagen

OOAD - Montgomery - Fall 2019

# OOAD-Semester-Project


This application streams video via TCP from a RaspberryPi, performs facial recognition on 
the stream, and displays output using PyQt5. Users can add and delete faces from a database 
and subscribe to receive SMS alerts for unknown faces on their phone.


### Requirements

This application uses Python3 and PyQt5.

Before the first run...

    $ cd OOAD-Semester-Project/
    $ mkdir data
    
Necessary Packages (not included in Python standard library)...

    PyQt5
    face_recognition
    dlib
    numpy
    cv2
    
These may all be installed via pip3. Dlib may optionally be installed with GPU support 
for faster facial recognition.


### Running the application

    $ cd src/
    $ python3 app.py
    
More information can be found in the design folder and our final report. Enjoy! :)