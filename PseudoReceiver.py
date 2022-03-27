import socket
import sys
from datetime import datetime

import cv2
import pickle
import numpy as np
import struct ## new

import Receiver
from Packet import Packet_Structure
flag = True
diff = []


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def face_detector_test(cloud_socket, image):
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
        global flag
        if flag:
            global diff
            diff = image
            flag = False
        if (mse(diff,image)) > 3000:
            diff = image
        # print(type(roi_color))
        # print(len(face_list))
            print("[INFO] Object found. Saving locally.")
            # cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
            if roi_color is not None:
                packetize_images(cloud_socket,roi_color)

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

def packetize_images(s,faces):

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    packet = Packet_Structure('192.168.07', len(faces), faces, '0011', str(current_time), 0)
    data_string = pickle.dumps(packet)
    # s.send(data_string)
    s.sendall(struct.pack("L", len(data_string))+data_string)


# def run(self):
#     # face_list = self.face_detector()
#     # self.catch_faceList(face_list)
#     # self.new_face_detector()
#     self.start_face_detection()
if __name__ == '__main__':

    HOST=''
    PORT=8089

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print ('Socket created')

    s.bind((HOST,PORT))
    print ('Socket bind complete')
    s.listen(10)
    print ('Socket now listening')

    conn,addr=s.accept()

    ### new
    data = b""
    payload_size = struct.calcsize("L")

    cloud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345

    cloud_socket.connect(('127.0.0.1', port))
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        ###

        frame=pickle.loads(frame_data)
        # print ("Hello")
        face_detector_test(cloud_socket, frame)