#!/usr/bin/env python
import re

# Code highly inspired from this github : github.com/abhishekkrthakur/isear/blob/master/server.py
#
#
#
import select, socket, sys
import socket, time, string
import random
from Crypto.Cipher import AES
from Element import Node
from Client_TOR import ClientTCP

# things to begin with
userNameList = []
passwordList = []


class Server(ClientTCP):

    def __init__(self, personal_ip, personal_port, message="".encode()):
        self.personal_ip = personal_ip
        self.personal_port = personal_port
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = message
        self.main()

    def random_token_generator(self, size=16, chars=string.ascii_uppercase + string.digits):
        print('begin random_token_generator')
        for i in range(size):
            return ''.join(random.choice(chars))

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
            if username in userNameList:
                print("Username already in use")
            else:
                userNameList.append(username)
                passwordList.append(password)
                print("User created")

        elif loginOrRegister == '1':
            print("Login process")
            print("Logging in...")

            if (username in userNameList and password in passwordList and userNameList.index(
                    username) == passwordList.index(password)):
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
