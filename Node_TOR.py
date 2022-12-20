import socket
import threading
from Contact import Contact
from Contact_list import Contact_list

class Node_TOR:

    def __init__(self, personal_ip, personal_port):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    initial_contacts_from_server = Contact_list()
    contact_list = Contact_list()
    conenxions = []

    
    def new_contact(self,tuple_contact):
        new_contact = Contact(int(tuple_contact[0]),tuple_contact[1],tuple_contact[2])
        self.contact_list.append(new_contact)
        print(tuple_contact[2] + " has been added to your contacts!")


    def __handle_input_data(self,new_connexion_sock,new_connexion_ip):
        while True:
            data = new_connexion_sock.recv(1024).decode()
            if not data:
                break
            print(data)


    def __receive_data(self):
        #Queue for connection
        self.input_socket.listen(10)
        while True:
            #New connexion
            new_connexion_sock, new_connexion_ip = self.input_socket.accept()
            #Thread creation
            new_connexion_thread = threading.Thread(target=self.__handle_input_data,args=(new_connexion_sock,new_connexion_ip))
            new_connexion_thread.start()

            
    def __send_by_contact(self,contact,data):
        output_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        output_socket.connect((contact.ip,contact.port))
        output_socket.send(data.encode())
        

    def __send_by_ip(self,contact,data):
        pass


    #send to somone
    def __send():
        pass

    #Thread that send data to another peer
    def __send_data(self):
        while True:
            message = input()
            parsed_message = self.__parse_message(message)
            
            if self.contact_list.find_by_name(parsed_message[0]) == None and self.node_list.find_by_ip(parsed_message[0]) == None:
                print(parsed_message[0] + " ne fait pas partit de votre liste de contacts")
            elif self.contact_list.find_by_name(parsed_message[0]) != None:
                self.__send_by_contact(self.contact_list.find_by_name(parsed_message[0]),parsed_message[1])
            elif self.node_list.find_by_ip(parsed_message[0]) != None:
                self.__send_by_ip(parsed_message[0],parsed_message[1])
             

    
    #When user enter a message he must do it with the structure "destination_name message"
    #This function parse the message to separate the name of the destination and the message content
    def __parse_message(self,message):
        split_index =message.index(" ")
        splitted_token = message.split(" ")
        return (splitted_token[0],message[split_index + 1:])


    def start(self):
        friend_port = 0
        if self.personal_port == 5000:
            friend_port = 5001
        else:
            friend_port = 5000

        self.contact_list.append(Contact(friend_port,'localhost',"Friend"))
        self.input_socket.bind((self.personal_ip, self.personal_port))
        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()
        self.initial_contacts_from_server = [] #TODO recevoir

        send_thread = threading.Thread(target=self.__send_data)
        send_thread.start()