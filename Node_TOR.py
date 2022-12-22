import re
import socket
import threading
from Element import Node

# TOR node that can receive data from other nodes and send data to other nodes/peers
class Node_TOR(Node):


    # Resend data to the next node
    def manage_data(self, data):
        print('entering manage_data :', data)
        ip, port, message = self.pop_header(data)
        ip = ip.decode()
        port = port.decode()
        port = int(port)
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

    def pop_header(self,plaintext):
        headerInPlaintext = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9}', plaintext)  # search for a header
        header = headerInPlaintext.group(0)  # extract the header
        searchIP = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', header)
        ip = searchIP.group(0)  # extract the header
        port = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//', header)
        port = port[1]  # extract the header
        splitHeaderPlaintext = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', plaintext,1)  # separate the header from the payload
        restPlaintext = splitHeaderPlaintext[1]  # keep the payload
        return (ip, port, restPlaintext)