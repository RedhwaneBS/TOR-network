#!/usr/bin/env python

# Code highly inspired from this github : github.com/abhishekkrthakur/isear/blob/master/server.py
#
#
#
import select, socket, sys
import socket, time, string
import random
from Crypto.Cipher import AES

# things to begin with
userNameList = []
passwordList = []


def Tcp_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HostIp, Port))
    return


def Tcp_server_wait(numOfClientWait, port, HostIp):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HostIp, port))
    s.listen(numOfClientWait)


def Tcp_server_next():
    global s
    s = s.accept()[0]


def write(message, connection):
    connection.send((message + '\n').encode())
    return


def receive(server):
    char = ''
    message = ''
    while char != '\n':
        char = (server.recv(1)).decode()
        message += char
    return message


def close():
    server.close()
    return


def random_token_generator(size=16, chars=string.ascii_uppercase + string.digits):
    print('begin random_token_generator')
    for i in range(size):
        return ''.join(random.choice(chars))


def authentification(s, connection, client_address, username, password, loginOrRegister):
    print('begin authentification')
    print('loginOrRegister is', loginOrRegister)
    loginOrRegister = loginOrRegister.strip()
    if loginOrRegister == '0':
        print("Creating new user")
        write("Registering...", connection)
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

        write(existence, connection)

        if existence == '0':
            print('existence sent')

            # Ancienne partie token
            # random_token = random_token_generator()
            random_token = b'Sixteen byte key'
            print('random :', random_token)
            connection.send(random_token)
            print('random_token sent')
            print("password : ", password)

            obj = AES.new(random_token, AES.MODE_EAX)
            ciphertext, tag = obj.encrypt_and_digest(password)
            nonce = obj.nonce
            connection.send(nonce)
            print('ciphertext :', ciphertext)

            # Déchiffrement du message token
            read_encrypted_hash = connection.recv(1024)
            print('read_encrypted_hash :', read_encrypted_hash)
            #read_encrypted_hash = read_encrypted_hash.strip('\n')

            if read_encrypted_hash == ciphertext:
                print("Authentication successful!")
                print(read_encrypted_hash, ciphertext)
                write("Successful", connection)
            else:
                print("Password mismatch!")
                write("Wrong Password", connection)
    else:
        print("Pass")
        pass

    print("--- Connection ended ---")


def main():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 17092))
    server.listen(5)
    inputsSocketList = [server]
    outputsSocketList = []
    message_queues = {}
    while inputsSocketList:
        readable, writable, exceptional = select.select(inputsSocketList, outputsSocketList, outputsSocketList)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                print(client_address, connection)
                if connection:
                    inputsSocketList.append(connection)
                    write('Welcome to the server. Please type your username and password to login.', connection)
                    print('first message', connection.recv(1024).decode())
                    username = receive(connection).strip('\n')
                    print(username)
                    password = connection.recv(1024)
                    print(password)
                    write('is it for login or register?', connection)
                    loginOrRegister = receive(connection).strip('\n')
                    print(loginOrRegister)
                    authentification(s, connection, client_address, username, password, loginOrRegister)
                    inputsSocketList.remove(connection)


if __name__ == '__main__':
    main()
