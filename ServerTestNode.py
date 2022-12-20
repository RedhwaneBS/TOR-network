#!/usr/bin/env python

# Code highly
#
#
#
import select, socket, sys
from queue import *
import socket, time, string
import sqlite3
import random

#from Crypto.Cipher import AES

from TORServer import TORServer


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

            random_token = random_token_generator()
            print('random :', random_token)
            write(random_token, connection)
            print('random_token sent')
            ciphertext = random_token
            obj = AES.new(random_token, AES.MODE_CBC, 'This is an IV456')
            ciphertext = obj.encrypt(password)
            read_encrypted_hash = receive(connection).strip('\n')
            print('read_encrypted_hash :', read_encrypted_hash)
            read_encrypted_hash = read_encrypted_hash.strip('\n')
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
    server.bind(('127.0.0.1', 17093))
    server.listen(5)
    server = TORServer()
    server.start()
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
                    username = receive(connection).strip('\n')
                    print(username)
                    password = receive(connection).strip('\n')
                    print(password)
                    write('is it for login or register?', connection)
                    loginOrRegister = receive(connection).strip('\n')
                    print(loginOrRegister)
                    authentification(s, connection, client_address, username, password, loginOrRegister)
                    inputsSocketList.remove(connection)
                    # Start authentification
            else:
                data = receive(server)
                # Resend data
                if data:
                    message_queues[s].put(data)
                    if s not in outputsSocketList:
                        outputsSocketList.append(s)
                else:
                    if s in outputsSocketList:
                        outputsSocketList.remove(s)
                    inputsSocketList.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            break
            try:
                next_msg = message_queues[s].get_nowait()
            except Empty:
                outputsSocketList.remove(s)
            else:
                s.send(next_msg)


if __name__ == '__main__':
    main()
