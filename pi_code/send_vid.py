#!/usr/bin/env python3
from picamera import PiCamera
from time import sleep
import socket

def main():

    with PiCamera() as camera:
        #camera.start_preview()
        #camera.start_recording('/home/pi/Desktop/py_test.h264')
        #sleep(5)
        #camera.stop_recording()
        #camera.stop_preview()
        #context = zmq.Context()
        #footage_socket = context.socket(zmq.PUB)
        #footage_socket = connect('tcp://localhost:8001')
        camera.resolution = (640, 480)
        camera.framerate = 5
        TCP_socket = socket.socket()
        TCP_socket.bind(("0.0.0.0", 8001))
        client_address = "10.0.0.115"
        TCP_socket.listen(0)
        conn = TCP_socket.accept()[0].makefile('wb')
        try:
            camera.start_recording(conn, format='h264')
            camera.wait_recording(180)
            camera.stop_recording()
        finally:
            conn.close()
            TCP_socket.close()




if __name__ == "__main__":
    main()
