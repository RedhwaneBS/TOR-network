import socket
import threading
from Node import Node

# TOR node that can receive data from other nodes and send data to other nodes/peers
class Node_TOR(Node):


    # Resend data to the next node
    def manage_data(self, data):
        print(data)
        ip, result = data.split("//", 1)
        port, message = result.split(" ", 1)
        port = int(port)
        print("ip: " + ip + " port: " + str(port) + " message: " + message)
        self.send(ip, port, message)


    # Allow to stop the program by typing "stop" in the console
    def take_input(self):
        while self.run:
            message = input()
            print(message)
            if message == "stop":
                print("Closing connection")
                self.input_socket.close()
                self.run = False



