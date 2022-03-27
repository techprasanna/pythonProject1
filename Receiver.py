import cv2
from threading import Thread
import numpy as np
import os
import socket
import pickle
from datetime import datetime
from Packet import Packet_Structure
import socket, threading

class Receiver(Thread):

    diff = 0
    counter = 0

    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)

    def run(self, clientAddress=None):
        # print ("Connection from : ", clientAddress)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        # Instead of this while True method, now we have to perform face detection
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
                break
            print("from client", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Client at ", clientAddress, " disconnected...")

    def face_detector_test(self, image):
        # imagePath = "/Users/prasannasmac/Documents/Capstone/test_image3.jpeg"

        # image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )

        # print("[INFO] Found {0} Faces.".format(len(faces)))
        # print(len(self.face_list))
        # print(faces)
        face_list = []
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_color = image[y:y + h, x:x + w]
            face_list.append(roi_color)
            # print(len(face_list))
            print("[INFO] Object found. Saving locally.")
            cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
            if roi_color is not None:
                self.packetize_images(roi_color)

        # status = cv2.imwrite('faces_detected.jpg', image)
        # print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
        # return face_list, faces
    # def catch_faceList(self, alist):
    #     print(alist)
    #     print(len(alist))

    # def start_face_detection(self):
    #     # faces = self.face_detector_test()
    #
    #     # print(len(faces))
    #     # cv2.imwrite(self.id+'faces.jpg', face_list[0])
    #
    #     if(len(faces) > 0):
    #         self.packetize_images(faces)

    def packetize_images(self, faces):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 12345

        s.connect(('127.0.0.1', port))
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        packet = Packet_Structure('192.168.07', len(faces), faces, '0011',str(current_time), 0)
        data_string = pickle.dumps(packet)
        s.send(data_string)

    # def run(self):
    #     # face_list = self.face_detector()
    #     # self.catch_faceList(face_list)
    #     # self.new_face_detector()
    #     self.start_face_detection()


