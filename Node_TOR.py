import socket
import threading
from Node import Node

class Node_TOR(Node):
    

    def __manage_data(self,data):
            print(data)
            ip, result = data.split("//", 1)
            port, message = result.split(" ", 1)
            port = int(port)
            print("ip: " + ip + " port: " + str(port) + " message: " + message)
            self.__send_by_ip_port(ip, port, message)


    def __take_input(self):
        while self.run:
            message = input()
            print(message)
            if message == "stop":
                print("Closing connection")
                self.input_socket.close()
                self.run = False



