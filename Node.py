import socket
import threading


class Node:

    def __init__(self, personal_ip, personal_port):
        self.personal_ip = personal_ip
        personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    node_list = []


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
        self.__send(contact.ip,contact.port,data,output_socket)
        

    def __send_by_ip(self,ip,data):
        output_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        contact = self.contact_list.find_by_ip(ip)
        self.__send(contact.ip,contact.port,data,output_socket)
    

    #send to somone
    def __send(self,ip,port,data,output_socket):
        output_socket.connect((ip,port))
        output_socket.send(data.encode())

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

        self.input_socket.bind((self.personal_ip, self.personal_port))
        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()

        send_thread = threading.Thread(target=self.__send_data)
        send_thread.start()

