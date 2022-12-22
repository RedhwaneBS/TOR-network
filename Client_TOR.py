import os
import socket
import threading
import random
import re
import pickle
import time

from Crypto.Cipher import AES

from Contact import Contact
from Contact_list import Contact_list
from Element import Element
import random


# TCP client that can send and receive data via a Tor network
class Client_TOR(Element):

    # Initialize the client with himself in his list of peers and the ip/port of the enter node of the Tor network
    def __init__(self, personal_ip, personal_port, connexion_ip, connexion_port):
        super().__init__(personal_ip, personal_port)
        # Coordinates of the enter node of the Tor network
        self.connexion_tuple = (connexion_ip, connexion_port)
        self.list_of_clients = [(self.personal_ip, self.personal_port,self.crypt.public_key)]


    # List of contacts to allow to send message easly by name
    contact_list = Contact_list()
    UsernameList = []
    PasswordList = []

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
        header_test = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', data)  # search for a header
        if header_test != None: 
            header = header_test.group(0)  # extract the header
            if header.decode() == "300.0.0.0//0 ":
                body = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', data)  # search for a header
                list_of_nodes = body[1]  # extract the list of nodes
                self.list_of_nodes = pickle.loads(list_of_nodes)  # load the list of nodes
                print("List of nodes received")
            if header.decode() == "300.0.0.0//1 ":
                body = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', data)  # search for a header
                list_of_clients = body[1]  # extract the list of clients
                self.list_of_clients += pickle.loads(list_of_clients)  # load the list of clients
                print(self.list_of_clients)
        else:
            print(data)

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
                    while self.run:
                        # Thread creation
                        print("thread created for server request")
                        new_connexion_thread = threading.Thread(target=self.connection_to_server())
                        new_connexion_thread.start()
                else:
                    message_with_path_header = self.create_message(self.randomiser(self.list_of_nodes), message)
                    print('message :',message_with_path_header)
                    parsed_message = self.__parse_message(message_with_path_header)
                    ip, port = parsed_message[0].split("//")
                    print('ip :',ip, 'port :',port, 'data :',parsed_message[1])
                    self.send(ip, int(port), parsed_message[1].encode())

    # When user enter a message he must do it with the structure "destination_name message"
    # This function parse the message to separate the name of the destination and the message content
    def __parse_message(self, message):
        split_index = message.index(" ")
        splitted_token = message.split(" ")
        return (splitted_token[0], message[split_index + 1:])

    # Connection to the server functions
    def connect(self, HostIp, Port):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HostIp, Port))
        return

    def create_message_from_bytes(self,path, message):
        nodes_string = ""
        for node in path:
            nodes_string += f"{node[0]}//{node[1]} "
        nodes_string_bytes = nodes_string.encode()
        return nodes_string_bytes + message


    def send_bytes(self, message):
        message_with_path_header = self.create_message_from_bytes(self.randomiser(self.list_of_nodes), message)
        s.send(message_with_path_header)


    def send_string_bytes(self, message):
        self.send_bytes(message.encode())


    def receive(self):
        char = ''
        message = ''
        while char != '\n':
            char = (s.recv(1)).decode()
            message += char
        return message


    def close(self):
        s.close()
        return


    def PasswordCreate(self):
        random_key = os.urandom(16)
        return random_key


    def connection_to_server(self):
        while self.run:
            ip_server = "127.0.0.1"
            port_server = 17092
            self.connect(ip_server, 17092)
            print(self.receive())
            username = input("Enter your username: ")
            self.send_string_bytes(username)
            if username in self.UsernameList:
                print("Username already exists")
                index = self.UsernameList.index(username)
                password = self.PasswordList[index]
            else:
                password = self.PasswordCreate()
                self.UsernameList.append(username)
                self.PasswordList.append(password)

            print("Password: ", password)
            self.send_bytes(password)
            print(self.receive())
            option = input('Type 1 for login or 0 for register: ')
            self.send_string_bytes(option)
            if option == '0':
                print('Registration sent')
            elif option == '1':
                existence = self.receive()
                existence = existence.strip('\n')
                print('Existence :', existence)
                false = '1'
                if existence == false:
                    print("Username or password is incorrect")
                    self.close()
                else:
                    # Partie token
                    random_token = s.recv(1024)
                    print("Random token :", random_token)
                    print("password : ", password)
                    nonce = s.recv(1024)
                    obj = AES.new(random_token, AES.MODE_EAX, nonce=nonce)
                    ciphertext, tag = obj.encrypt_and_digest(password)

                    # Envoi du token chiffré
                    self.send_bytes(ciphertext)
                    print('cipher sent : ', ciphertext)
                    auth_stat = self.receive()
                    auth_stat = auth_stat.strip('\n')
                    print('auth_stat :', auth_stat)

            self.close()
            self.run = False


    def popIP(self,plaintext):
        print('plaintext :', plaintext)
        ipMatch = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', plaintext)  # search for an ip address
        ip = ipMatch.group(0).decode('utf8')  # extract the ip & in string$
        print('plaintext2 :', plaintext)
        print('ip :', ip)
        ipMatch = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}###',plaintext)  # separate the ip address from the payload
        ipMatch = ipMatch[1]  # keep the payload
        return (ip, ipMatch)


    def sharing_contacts(self):
        return super().sharing_contacts()
    
    def connect_to_TOR(self):
        socket_entering_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_entering_node.connect(self.connexion_tuple)
        socket_entering_node.send("300.0.0.0//0 ".encode() + pickle.dumps(self.list_of_clients[0]))
        socket_entering_node.close()


    def start(self):
        super().start()
        time.sleep(1)
        asking_nodes_thread = threading.Thread(target=self.connect_to_TOR)
        asking_nodes_thread.start()