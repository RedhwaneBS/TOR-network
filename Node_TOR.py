import re
import socket
import threading
from Node import Node

# TOR node that can receive data from other nodes and send data to other nodes/peers
class Node_TOR(Node):


    # Resend data to the next node
    def manage_data(self, data):
        print(data)
        head, message = self.popIP(data)
        ip, port = head.split("//", 1)
        port = int(port)
        print("ip: " + ip + " port: " + str(port) + " message: " + message)
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

    def popIP(self,plaintext):
        print('plaintext :', plaintext)
        ipMatch = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', plaintext)  # search for an Header address
        Header = ipMatch.group(0).decode('utf8')  # extract the Header & in string$
        
        ipMatch = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//.\d{0,9} ',plaintext)  # separate the Header address from the payload
        ipMatch = ipMatch[1]  # keep the payload
        return (Header, ipMatch)
