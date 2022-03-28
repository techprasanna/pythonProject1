import struct

import cv2
from threading import Thread
import numpy as np
import os
import socket
import pickle
from datetime import datetime
from Packet import Packet_Structure
import socket, threading
from main import Main
class Receiver(Thread):

    diff = 0
    counter = 0
    flag = True
    diff = []
    m = Main()

    def __init__(self, clientAddress, clientsocket, cloud_socket):
        threading.Thread.__init__(self)
        self.conn = clientsocket
        self.cloud_socket = cloud_socket
        self.clientAddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        data = b""
        payload_size = struct.calcsize("L")
        while True:
            while len(data) < payload_size:
                data += self.conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            ###

            frame = pickle.loads(frame_data)
            # print ("Hello")
            self.face_detector_test(frame)

    def face_detector_test(self,image):
        # imagePath = "/Users/prasannasmac/Documents/Capstone/test_image3.jpeg"

        # image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # global flag
        # if flag:
        #     global diff
        #     diff = image
        #     flag = False
        # print(mse(diff,image))
        # diff = image

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
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_color = image[y:y + h, x:x + w]
            face_list.append(roi_color)
            if self.flag:
                self.diff = image
                self.flag = False
            if (self.mse(self.diff, image)) > 3000:
                self.diff = image
                # print(type(roi_color))
                # print(len(face_list))
                print("[INFO] Object found. Saving locally.")
                # cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
                if roi_color is not None:
                    self.packetize_images(roi_color)

        # status = cv2.imwrite('faces_detected.jpg', image)
        # print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
        # return face_list, faces

    def packetize_images(self,faces):

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        packet = Packet_Structure(self.clientAddress, len(faces), faces, '0011', str(current_time), 0)
        data_string = pickle.dumps(packet)
        # s.send(data_string)
        self.m.add_data(self.cloud_socket, data_string)

    def mse(self, imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])

        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    # def run(self):
    #     # face_list = self.face_detector()
    #     # self.catch_faceList(face_list)
    #     # self.new_face_detector()
    #     self.start_face_detection()


