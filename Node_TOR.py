import socket
import threading
import pickle
from Element import Element

# TOR node that can receive data from other nodes and send data to other nodes/peers
class Node_TOR(Element):

    list_of_nodes = []

    # Resend data to the next node
    def manage_data(self, data):
        print(data)
        print("manage_data")
        ip, port, message = self.pop_header(data)
        ip = ip.decode()
        port = port.decode()
        # Special header 0//0 is for receiving a client coordinates
        if ip == "300.0.0.0" and port == "0":
            client = pickle.loads(message)
            print("New client")
            print(str(client[0]) + " " + str(client[1]))
            # Add the client to the list of clients
            self.list_of_clients.append(client)
            # Share the list of nodes from the TOR to the new client
            self.share_nodes(client)
        else:
            port = int(port)
            print("ip: " + ip + " port: " + str(port) + " message: " + message.decode())
            self.send(ip, port, message)

    # Send the list of nodes to a client
    def share_nodes(self, client):
        socket_node_sharing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_node_sharing.connect((client[0], int(client[1])))
        socket_node_sharing.send("300.0.0.0//0 ".encode() + pickle.dumps(self.list_of_nodes))
        print("DONE")
        socket_node_sharing.close()

    def encryption(self, data):
        pass

    def decryption(self, data):
        pass

    # Allow to stop the program by typing "stop" in the console
    def take_input(self):
        while self.run:
            message = input()
            print(message)
            if message == "stop":
                print("Closing connection")
                self.input_socket.close()
                self.run = False

