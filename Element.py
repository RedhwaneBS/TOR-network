import socket
import threading
import Cryptem
import os
import re
from RSA import decrypt_the_cipher

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
    # List of nodes TOR to create paths
    list_of_nodes = []
    # List of peers conncected to the network
    list_of_clients = []

    # Thread that receives data
    def __handle_input_data(self, new_connexion_sock, new_connexion_ip):
        while self.run:
            data = new_connexion_sock.recv(4096)
            if not data:
                break
            print(data)
            self.manage_data(data)
        new_connexion_sock.close()


    # Send data to another peer/node
    def send(self, ip, port, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_socket.connect((ip, port))
        output_socket.send(data)
        output_socket.close()

    # Thread that receives data from other peers simultaneously
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


    # Thread that sends data to another peer
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


    # Start the node
    def start(self):

        self.input_socket.bind((self.personal_ip, self.personal_port))
        print('Node started ' + " ip : " + self.personal_ip + " port : " + str(self.personal_port))
        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()

        receive_thread = threading.Thread(target=self.__send_data)
        receive_thread.start()

    # Parse the header
    def pop_header(self,plaintext):
        headerInPlaintext = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9}', plaintext)  # search for a header
        header = headerInPlaintext.group(0)  # extract the header
        searchIP = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', header)
        ip = searchIP.group(0)  # extract the IP
        port = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//', header)
        port = port[1]  # extract the port
        splitHeaderPlaintext = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', plaintext,1)  # separate the header from the payload
        restPlaintext = splitHeaderPlaintext[1]  # keep the payload
        print("header: " , header , " ip: " ,ip , " port: " , port , " message: " , restPlaintext)
        #print("header: " + header.decode() + " ip: " + ip.decode() + " port: " + port.decode() + " rest: " + restPlaintext.decode())
        return (ip, port, restPlaintext)