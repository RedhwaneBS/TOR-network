import os
import socket
import threading
import random
import re

from Crypto.Cipher import AES

from Contact import Contact
from Contact_list import Contact_list
from Element import Node
import random


# TCP client that can send and receive data via a Tor network
class ClientTCP(Node):
    # List of contacts
    contact_list = Contact_list()
    UsernameList = []
    PasswordList = []
    # List of nodes coordinates
    list_of_nodes = [("127.0.0.1", 6003), ("127.0.0.1", 6004), ("127.0.0.1", 6005), ("127.0.0.1", 6006),
                     ("127.0.0.1", 6007), ("127.0.0.1", 6008), ("127.0.0.1", 6009)]

    def __init__(self, personal_ip, personal_port, message="".encode()):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.personal_port_server = 7001
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = message

    # Creat a message with a path of nodes
    def create_message(self, path, message):
        nodes_string = ""
        for node in path:
            nodes_string += f"{node[0]}//{node[1]} "
        return f"{nodes_string}{message}"

    # Return a random list of node to create a path
    def randomiser(self, liste):
        # tire un nombre au hasard entre 0 et la longueur de la liste
        nombre = random.randint(1, len(liste) - 1)

        # retourne ce nombre d'éléments de la liste
        new_liste = random.sample(liste, nombre)
        return new_liste

    # add a contact to the contact list
    def new_contact(self, tuple_contact):
        new_contact = Contact(int(tuple_contact[0]), tuple_contact[1], tuple_contact[2])
        self.contact_list.append(new_contact)
        print(tuple_contact[2] + " has been added to your contacts!")

    # Print the data received
    def manage_data(self, data):
        pass

    # Parse the input to send data to another contact
    def take_input(self):

        while self.run:
            head_type = 0
            send_message = False
            message = input()
            head, data = self.__parse_message(message)
            head_parsed = head.split("//")
            if head_parsed != None:
                head_type = len(head_parsed)

            if head_type == 1:
                if head in self.contact_list.get_list_of_names():
                    contact = self.contact_list.get_contact_by_name(head)
                    message = f"{contact.ip}//{contact.port} " + data
                    send_message = True

                elif head == "add":
                    tuple_contact = data.split(" ")
                    self.new_contact(tuple_contact)

                else:
                    print(head + " is not in your contact list or is an ivalid input")
                    print(
                        "Please enter a valid input or add the contact to your contact list using the command 'add' [port] [ip] [name]")
            elif head_type != 2:
                print("Invalid input header")
                print("Please enter an input following the scheme ip//port message or contact_name message")
                print("You can add a contact to your contact list using the command 'add' [port] [ip] [name]")
            elif head_type == 2:
                send_message = True

            if send_message:
                if data == "Server Request":
                    self.connection_to_server()
                else:
                    message_with_path_header = self.create_message(self.randomiser(self.list_of_nodes), message)
                    print('message :', message_with_path_header)
                    parsed_message = self.__parse_message(message_with_path_header)
                    ip, port = parsed_message[0].split("//")
                    print('ip :', ip, 'port :', port, 'data :', parsed_message[1])
                    self.send(ip, int(port), parsed_message[1].encode())

    # When user enter a message he must do it with the structure "destination_name message"
    # This function parse the message to separate the name of the destination and the message content
    def __parse_message(self, message):
        split_index = message.index(" ")
        splitted_token = message.split(" ")
        return (splitted_token[0], message[split_index + 1:])

    # Connection to the server functions

    def create_message_from_bytes(self, path, message):
        nodes_string = ""
        for node in path:
            nodes_string += f"{node[0]}//{node[1]} "
        nodes_string_bytes = nodes_string.encode()
        return nodes_string_bytes + message

    def send_bytes(self, message, ip, port):
        message = (ip + "//" + str(port) + " ").encode() + (
                self.personal_ip + "//" + str(self.personal_port) + " ").encode() + message
        message_with_path_header = self.create_message_from_bytes(self.randomiser(self.list_of_nodes), message)
        print('message with path:', message_with_path_header)
        ip, port, message = self.pop_header(message_with_path_header)
        ip = ip.decode()
        port = int(port.decode())
        print('ip :', ip, 'port :', port, 'data :', message)
        self.send(ip, int(port), message)

    def send_string_bytes(self, message, ip, port):
        self.send_bytes(message.encode(), ip, port)

    def receive(self, s):
        data = s.recv(1024)
        return data

    def connect(self, HostIp, Port):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HostIp, Port))
        return s

    def close(self, s):
        s.close()
        return

    def PasswordCreate(self):
        random_key = os.urandom(16)
        return random_key

    def connection_to_server(self):
        while self.run:
            print("connection to server")
            print("My attributes are : ", self.personal_ip, self.personal_port)
            ip_server = "127.0.0.1"
            port_server = 17088
            self.connect(ip_server, port_server)
            print("connected to server")
            message_decode = self.receive(s).decode()
            print(message_decode)
            print("received")
            username = input("Enter your username: ")
            self.send_string_bytes(username, ip_server, port_server)
            if username in self.UsernameList:
                print("Username already exists")
                index = self.UsernameList.index(username)
                password = self.PasswordList[index]
            else:
                password = self.PasswordCreate()
                self.UsernameList.append(username)
                self.PasswordList.append(password)
            print("Password: ", password)
            self.send_bytes(password, ip_server, port_server)
            print(self.receive(s))
            option = input('Type 1 for login or 0 for register: ')
            self.send_string_bytes(option, ip_server, port_server)
            if option == '0':
                print('Registration sent')
            elif option == '1':
                existence = self.receive(s)
                existence = existence.decode()
                print('Existence :', existence)
                false = '1'
                if existence == false:
                    print("Username or password is incorrect")
                    self.close(s)
                else:
                    # Partie token
                    random_token = s.recv(1024)
                    print("Random token :", random_token)
                    print("password : ", password)
                    nonce = s.recv(1024)
                    obj = AES.new(random_token, AES.MODE_EAX, nonce=nonce)
                    ciphertext, tag = obj.encrypt_and_digest(password)

                    # Envoi du token chiffré
                    self.send_bytes(ciphertext, ip_server, port_server)
                    print('cipher sent : ', ciphertext)
                    auth_stat = self.receive(s)
                    auth_stat = auth_stat.strip('\n')
                    print('auth_stat :', auth_stat)

        self.close(s)
        self.run = False

    def __handle_input_data_from_server(self, new_connexion_sock, new_connexion_ip):
        while self.run:
            data = new_connexion_sock.recv(4096)
            if not data:
                break
            self.manage_data(data)
        new_connexion_sock.close()

    def pop_header(self, plaintext):
        headerInPlaintext = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9}', plaintext)  # search for a header
        header = headerInPlaintext.group(0)  # extract the header
        searchIP = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', header)
        ip = searchIP.group(0)  # extract the header
        port = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//', header)
        port = port[1]  # extract the header
        splitHeaderPlaintext = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', plaintext,
                                        1)  # separate the header from the payload
        restPlaintext = splitHeaderPlaintext[1]  # keep the payload
        return (ip, port, restPlaintext)

    # Gestion des threads
    def __receive_data_from_server(self):
        # Queue for connection
        self.input_socket.listen(10)
        while self.run:
            # New connexion
            new_connexion_sock, new_connexion_ip = self.server_socket.accept()
            # Thread creation
            new_connexion_thread = threading.Thread(
                target=self.__handle_input_data_from_server(), args=(new_connexion_sock, new_connexion_ip))
            new_connexion_thread.start()

    def start(self):

        self.input_socket.bind((self.personal_ip, self.personal_port))
        print('Node started ' + " ip : " + self.personal_ip + " port : " + str(self.personal_port))
        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()

        receive_thread = threading.Thread(target=self.__send_data)
        receive_thread.start()

        self.server_socket.bind((self.personal_ip, self.personal_port_server))
        server_thread = threading.Thread(target=self.__receive_data_from_server())
        server_thread.start()