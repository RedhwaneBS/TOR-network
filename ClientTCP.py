import socket
import threading
import random
from Contact import Contact
from Contact_list import Contact_list

class ClientTCP:
    def __init__(self, personal_ip, personal_port):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    bool = True
    initial_contacts_from_server = Contact_list()
    contact_list = Contact_list()
    list_of_nodes = [("127.0.0.1", 5003), ("127.0.0.1", 5004), ("127.0.0.1", 5005), ("127.0.0.1", 5006), ("127.0.0.1", 5007), ("127.0.0.1", 5008), ("127.0.0.1", 5009)]

    def create_message(self, path, message):
        nodes_string = ""
        for node in path:
            nodes_string += f"{node[0]}//{node[1]} "
        return f"{nodes_string}{message}"

    def randomiser(self, liste):
        # tire un nombre au hasard entre 0 et la longueur de la liste
        nombre = random.randint(1, len(liste) - 1)

        # retourne ce nombre d'éléments de la liste
        new_liste = random.sample(liste, nombre)
        return new_liste

    def new_contact(self, tuple_contact):
        new_contact = Contact(
            int(tuple_contact[0]), tuple_contact[1], tuple_contact[2])
        self.contact_list.append(new_contact)
        print(tuple_contact[2] + " has been added to your contacts!")

    def __handle_input_data(self, new_connexion_sock, new_connexion_ip):
        while bool:
            data = new_connexion_sock.recv(1024).decode()
            if not data:
                break
            print(data)
        new_connexion_sock.close()

    def __receive_data(self):
        # Queue for connection
        self.input_socket.listen(10)
        while bool:
            # New connexion
            new_connexion_sock, new_connexion_ip = self.input_socket.accept()
            # Thread creation
            new_connexion_thread = threading.Thread(
                target=self.__handle_input_data, args=(new_connexion_sock, new_connexion_ip))
            new_connexion_thread.start()

    def __send_by_contact(self, contact, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__send(contact.ip, contact.port, data, output_socket)

    def __send_by_ip_port(self, ip, port, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__send(ip, port, data, output_socket)

    # send to somone
    def __send(self, ip, port, data, output_socket):
        output_socket.connect((ip, port))
        output_socket.send(data.encode())
        output_socket.close()

    # Thread that send data to another peer
    def __send_data(self):
        try:
            while True:
                message = input()
                data = self.create_message(self.randomiser(self.list_of_nodes), message)
                print(data)
                parsed_message = self.__parse_message(data)
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
            self.bool = False
            self.input_socket.close()
            print('interrupted!')

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


