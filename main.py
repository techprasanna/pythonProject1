import struct
import time
from Packet import Packet_Structure
from threading import Thread
import Receiver
import socket
import socket, threading

class Main():
    queue = []
    threadLock = threading.Lock()

    def send_data(self, cloud_socket, packet):
        self.threadLock.acquire()
        cloud_socket.sendall(struct.pack("L", len(packet)) + packet)
        self.queue.pop(0)
        self.threadLock.release()

    def add_data(self, cloud_socket, packet):
        self.queue.append(packet)
        while len(self.queue) != 0:
            self.send_data(cloud_socket, self.queue[0])



    if __name__ == '__main__':
        #Sending data to cloud. Used cloud socket to transfer images to cloud server. Port = 12345
        cloud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 12345
        cloud_socket.connect(('127.0.0.1', port))

        # Receiving Data from the edge device
        LOCALHOST = "127.0.0.1"
        PORT = 8089
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        print("Server started")
        print("Waiting for client request..")
        while True:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            newthread = Receiver.Receiver(clientAddress, clientsock, cloud_socket)
            newthread.start()
        # receiver = Receiver('127.0.0.1',"Prasanna")
        # receiver.start()
        # obj = Packet_Structure("192.1.0.1", "4", "NULL","1009", "Hello","0")

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
