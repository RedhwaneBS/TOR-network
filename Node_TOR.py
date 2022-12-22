import re
import socket
import threading
from Element import Element
from RSA import decrypt_the_cipher, pop_header


# TOR node that can receive data from other nodes and send data to other nodes/peers
class Node_TOR(Element):

    list_of_nodes = []

    # Resend data to the next node
    def manage_data(self, data):
        data = decrypt_the_cipher(self.crypt, data)
        print(data)
        (ip, port, message) = pop_header(data)
        ip = ip.decode()
        port = port.decode()
        port = int(port)
        print("ip: " + ip + " port: " + str(port) + " message: " + message.decode())
        self.send(ip, port, message)

    def encryption(self, data):
        pass

    def decryption(self, data):
        pass

    # Allow to stop the program by typing "stop" in the console
    def take_input(self):
        while self.run:
            message = input()
            print(message)
            if message == "stop":
                print("Closing connection")
                self.input_socket.close()
                self.run = False