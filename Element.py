import socket
import threading
import Cryptem
import os

# Node that can receive data from other nodes and send data to other nodes
class Element:

    # Constructor
    def __init__(self, personal_ip, personal_port):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.crypt = Cryptem.Crypt()
        print(self.crypt.public_key)

    # Boolean to stop the program
    run = True
    list_of_nodes = []


    # Thread that receive data
    def __handle_input_data(self, new_connexion_sock, new_connexion_ip):
        while self.run:
            data = new_connexion_sock.recv(4096)
            if not data:
                break
            self.manage_data(data)
        new_connexion_sock.close()


    # Send data to another peer/node
    def send(self, ip, port, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_socket.connect((ip, port))
        output_socket.send(data)
        output_socket.close()

    # Thread that receive data from other peers simultaneously
    def __receive_data(self):
        # Queue for connection
        self.input_socket.listen(10)
        while self.run:
            # New connexion
            new_connexion_sock, new_connexion_ip = self.input_socket.accept()
            # Thread creation
            new_connexion_thread = threading.Thread(
                target=self.__handle_input_data, args=(new_connexion_sock, new_connexion_ip))
            new_connexion_thread.start()

    # Manage data received
    def manage_data(self, data):
        raise NotImplementedError


    # Thread that send data to another peer
    def __send_data(self):
        try:
            self.take_input()
        except KeyboardInterrupt:
            with open('public_keys.csv', 'w') as f:
                f.write('')
            self.run = False
            self.input_socket.close()
            print('interrupted!')
            self.run = False
            self.input_socket.close()
            print('interrupted!')

    # Take input from user
    def take_input(self):
        raise NotImplementedError

    # Thread that shar coordonates from nodes in its node list
    def sharing_node(self):
        pass

    # Start the node
    def start(self):

        self.input_socket.bind((self.personal_ip, self.personal_port))
        print('Node started ' + " ip : " + self.personal_ip + " port : " + str(self.personal_port))
        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()

        receive_thread = threading.Thread(target=self.__send_data)
        receive_thread.start()

