import time
from Packet import Packet_Structure
from threading import Thread
from Receiver import Receiver
import socket
import socket, threading

class Main():
    queue = []

    def send_data(self):
        if(len(self.queue)) != 0:
            return self.queue.pop(0)
        else:
            return None

    def add_data(self, packet):
        self.queue.append(packet)

    if __name__ == '__main__':
        LOCALHOST = "127.0.0.1"
        PORT = 8080
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        print("Server started")
        print("Waiting for client request..")
        while True:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            newthread = Receiver(clientAddress, clientsock)
            newthread.start()
        # receiver = Receiver('127.0.0.1',"Prasanna")
        # receiver.start()
        # obj = Packet_Structure("192.1.0.1", "4", "NULL","1009", "Hello","0")

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
