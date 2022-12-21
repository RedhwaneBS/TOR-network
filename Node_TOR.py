import socket
import threading
from Contact import Contact
from Contact_list import Contact_list


class Node_TOR:

    def __init__(self, personal_ip, personal_port):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bool = True
    initial_contacts_from_server = Contact_list()
    contact_list = Contact_list()
    connexions = []

    def new_contact(self, tuple_contact):
        new_contact = Contact(int(tuple_contact[0]), tuple_contact[1], tuple_contact[2])
        self.contact_list.append(new_contact)
        print(tuple_contact[2] + " has been added to your contacts!")

    def __handle_input_data(self, new_connexion_sock, new_connexion_ip):
        while bool:
            data = new_connexion_sock.recv(1024).decode()
            if not data:
                break
            print(data)
            ip, result = data.split("//", 1)
            port, message = result.split(" ", 1)
            port = int(port)
            print("ip: " + ip + " port: " + str(port) + " message: " + message)
            self.__send_by_ip_port(ip, port, message)
            ##print(data)

        new_connexion_sock.close()

    def __receive_data(self):
        # Queue for connection
        self.input_socket.listen(10)
        while bool:
            # New connexion
            new_connexion_sock, new_connexion_ip = self.input_socket.accept()
            # Thread creation
            new_connexion_thread = threading.Thread(target=self.__handle_input_data,
                                                    args=(new_connexion_sock, new_connexion_ip))
            new_connexion_thread.start()

    def __send_by_contact(self, contact, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_socket.connect((contact.ip, contact.port))
        output_socket.send(data.encode())

    def __send_by_ip_port(self, ip, port, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__send(ip, port, data, output_socket)

    def __send(self, ip, port, data, output_socket):
        output_socket.connect((ip, port))
        output_socket.send(data.encode())
        output_socket.close()


    # Thread that send data to another peer
    def __send_data(self):
        try:
            while True:
                message = input()
                parsed_message = self.__parse_message(message)
                if "//" in parsed_message[0]:
                    ip, port = parsed_message[0].split("//")
                    self.__send_by_ip_port(ip, int(port), parsed_message[1])
                else:
                    contact = self.contact_list.find_by_name(parsed_message[0])
                    if contact != None:
                        self.__send_by_contact(contact, parsed_message[1])
                    else:
                        print("Contact not found")
        except KeyboardInterrupt:
            print("Closing connection")
            self.input_socket.close()


    # When user enter a message he must do it with the structure "destination_name message"
    # This function parse the message to separate the name of the destination and the message content
    def __parse_message(self, message):
        split_index = message.index(" ")
        splitted_token = message.split(" ")
        return (splitted_token[0], message[split_index + 1:])

    def start(self):
        friend_port = 0
        if self.personal_port == 5000:
            friend_port = 5001
        else:
            friend_port = 5000

        self.contact_list.append(Contact(friend_port, 'localhost', "Friend"))
        self.input_socket.bind((self.personal_ip, self.personal_port))
        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()
        self.initial_contacts_from_server = []  # TODO recevoir

        send_thread = threading.Thread(target=self.__send_data)
        send_thread.start()
