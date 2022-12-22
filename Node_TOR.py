import socket
import threading
import pickle
import random
import time
import re
from Element import Element
from RSA import decrypt_the_cipher, pop_header


# TOR node that can receive data from other nodes and send data to other nodes/peers
class Node_TOR(Element):

    list_of_nodes = []

    # Resend data to the next node
    def manage_data(self, data):
        header_test = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', data)

        if header_test is None:
            data = decrypt_the_cipher(self.crypt, data)

        print(data)
        (ip, port, message) = pop_header(data)

        #ip, port, message = pop_header(data)
        ip = ip.decode()
        port = port.decode()
        # Special header 300.0.0.0//0 is for receiving a client coordinates
        if ip == "300.0.0.0" and port == "0":
            client = pickle.loads(message)
            print("New client")
            print(str(client[0]) + " " + str(client[1]))
            # Add the client to the list of clients
            self.list_of_clients.append(client)
            # Share the list of nodes from the TOR to the new client
            self.share_nodes(client)
        # Special header 300.0.0.0//1 is for receiving a list of clients
        elif ip == "300.0.0.0" and port == "1":
            clients = pickle.loads(message)
            self.list_of_clients += clients
            print("Clients shared")
        else:
            port = int(port)
            print("ip: " + ip + " port: " + str(port) + " message: " + str(pickle.loads(message)))
            self.send(ip, port, message)

    # Send the list of nodes to a client
    def share_nodes(self, client):
        socket_node_sharing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_node_sharing.connect((client[0], int(client[1])))
        socket_node_sharing.send("300.0.0.0//0 ".encode() + pickle.dumps(self.list_of_nodes))
        print("DONE")
        socket_node_sharing.close()

    # Allow to stop the program by typing "stop" in the console
    def take_input(self):
        while self.run:
            message = input()
            print(message)
            if message == "stop":
                print("Closing connection")
                self.input_socket.close()
                self.run = False

    # Thread that share coordonates from nodes in its node list
    def sharing_contacts_between_nodes(self):
        while self.run:
            time.sleep(10)
            if self.list_of_clients != []:
                share_list = random.sample(self.list_of_clients,len(self.list_of_clients))
                for node in self.list_of_nodes:
                    self.send(node[0], int(node[1]),"300.0.0.0//1 ".encode() + pickle.dumps(share_list))
            if len(self.list_of_clients) > 5:
                self.list_of_clients = random.sample(self.list_of_clients, 3)
            


    # Thread that send clients coordonates to the other clients
    def sharing_contacts_between_clients(self):
        while self.run:
            time.sleep(5)
            print("Sharing contacts")
            print(self.list_of_clients)
            if self.list_of_clients != []:
                share_list = random.sample(self.list_of_clients,len(self.list_of_clients))
                for client in share_list:
                    self.send(client[0], int(client[1]),"300.0.0.0//1 ".encode() + pickle.dumps(share_list))
            if len(self.list_of_clients) > 5:
                self.list_of_clients = random.sample(self.list_of_clients, 3)
            


    def __init__(self, personal_ip, personal_port):
        super().__init__(personal_ip, personal_port)
        sharing_thread_nodes = threading.Thread(target=self.sharing_contacts_between_nodes)
        sharing_thread_nodes.start()
        sharing_thread_clients = threading.Thread(target=self.sharing_contacts_between_clients)
        sharing_thread_clients.start()
