import socket
import threading

# Node that can receive data from other nodes and send data to other nodes
class Node:
    
    def __init__(self, personal_ip, personal_port):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    run = True

    def __handle_input_data(self, new_connexion_sock, new_connexion_ip):
        while self.run:
            data = new_connexion_sock.recv(1024).decode()
            if not data:
                break
            self.manage_data(data)
        new_connexion_sock.close()

    def send_by_ip_port(self, ip, port, data):
        self.__send(ip, port, data)

    def __send(self, ip, port, data):
        output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_socket.connect((ip, port))
        output_socket.send(data.encode())
        output_socket.close()


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

    def manage_data(self, data):
        raise NotImplementedError

    # Thread that send data to another peer
    def __send_data(self):
        try:
            self.take_input()
        except KeyboardInterrupt:
            self.run = False
            self.input_socket.close()
            print('interrupted!')
    
    def take_input(self):
        raise NotImplementedError

    def start(self):

        self.input_socket.bind((self.personal_ip, self.personal_port))

        receive_thread = threading.Thread(target=self.__receive_data)
        receive_thread.start()

        receive_thread = threading.Thread(target=self.__send_data)
        receive_thread.start()