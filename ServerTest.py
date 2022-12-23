#!/usr/bin/env python
import pickle
import re

# Code highly inspired from this github : github.com/abhishekkrthakur/isear/blob/master/server.py
#
#
#
import select, socket, sys
import socket, time, string
import random
from Crypto.Cipher import AES
from Element import Element
from Client_TOR import Client_TOR

# things to begin with



class Server(Client_TOR):

    def __init__(self, personal_ip, personal_port, connexion_ip, connexion_port):
        super().__init__(personal_ip, personal_port)
        # Coordinates of the enter node of the Tor network
        self.connexion_tuple = (connexion_ip, connexion_port)
        self.list_of_clients = [(self.personal_ip, self.personal_port,self.crypt.public_key)]
        self.userNameList = []
        self.passwordList = []


    def random_token_generator(self, size=16, chars=string.ascii_uppercase + string.digits):
        print('begin random_token_generator')
        for i in range(size):
            return ''.join(random.choice(chars))

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
            if header.decode() == "300.0.0.0//2 ":
                pass

        else:
            print(data.decode())
            pass
    def main(self):
        print("Server started")
        global server_socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 17088))
        server_socket.listen(5)
        inputsSocketList = [server_socket]
        outputsSocketList = []
        while inputsSocketList:
            readable, writable, exceptional = select.select(inputsSocketList, outputsSocketList, outputsSocketList)
            for s in readable:
                if s is server_socket:
                    connection, client_address = server_socket.accept()
                    ip_client = client_address[0]
                    port_client = client_address[1]
                    print("Connection from", ip_client, port_client)
                    if connection:
                        inputsSocketList.append(connection)
                        self.send_bytes('Welcome to the server. Please type your username and password to login.'.encode(),ip_client, port_client)
                        print("welcome sent")
                        username = self.receive(connection)
                        print(username.decode())
                        password = self.receive(connection)
                        print(password)
                        self.send_bytes('is it for login or register?'.encode(), ip_client, port_client)
                        loginOrRegister = self.receive(connection)
                        print(loginOrRegister.decode())
                        self.authentification(connection, username, password, loginOrRegister, ip_client, port_client)
                        inputsSocketList.remove(connection)

    def authentification(self, connection, username, password, loginOrRegister, ip_client, port_client):
        print('begin authentification')
        print('loginOrRegister is', loginOrRegister)
        loginOrRegister = loginOrRegister.decode()
        if loginOrRegister == '0':
            print("Creating new user")
            self.send_bytes("Registering...".encode(), ip_client, port_client)
            if username in self.userNameList:
                print("Username already in use")
            else:
                self.userNameList.append(username)
                self.passwordList.append(password)
                print("User created")

        elif loginOrRegister == '1':
            print("Login process")
            print("Logging in...")

            if (username in self.userNameList and password in self.passwordList and self.userNameList.index(
                    username) == self.passwordList.index(password)):
                existence = '0'
            else:
                existence = '1'

            self.send_bytes(existence.encode(), ip_client, port_client)

            if existence == '0':
                print('existence sent')

                # Ancienne partie token
                # random_token = random_token_generator()
                random_token = b'Sixteen byte key'
                print('random :', random_token)
                self.send_bytes(random_token, ip_client, port_client)
                print('random_token sent')
                print("password : ", password)

                obj = AES.new(random_token, AES.MODE_EAX)
                ciphertext, tag = obj.encrypt_and_digest(password)
                nonce = obj.nonce
                self.send_bytes(nonce, ip_client, port_client)
                print('ciphertext :', ciphertext)

                # Déchiffrement du message token
                read_encrypted_hash = self.receive(connection)
                self.send_bytes(read_encrypted_hash, ip_client, port_client)
                print('read_encrypted_hash :', read_encrypted_hash)
                # read_encrypted_hash = read_encrypted_hash.strip('\n')

                if read_encrypted_hash == ciphertext:
                    print("Authentication successful!")
                    print(read_encrypted_hash, ciphertext)
                    self.send_bytes("Successful".encode(), ip_client, port_client)
                else:
                    print("Password mismatch!")
                    self.send_bytes("Wrong Password".encode(), ip_client, port_client)
        else:
            print("Pass")
            pass

        print("--- Connection ended ---")

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


client = Server("127.0.0.1", 17090)
