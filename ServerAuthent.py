#!/usr/bin/env python

# Code highly inspired from: github.com/bozhu/AES-Python/blob/master/aes.py
#
#
#
import select, socket, sys
from queue import *
import socket, time, string
import sqlite3
import random
#from crypto.Cipher import AES
import TORServer

# things to begin with

def Tcp_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HostIp, Port))
    return


def Tcp_server_wait(numOfClientWait, port, HostIp):
    global s2
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s2.bind((HostIp, port))
    s2.listen(numOfClientWait)


def Tcp_server_next():
	global s
	s = s2.accept()[0]

def write(message):
    s.send(message + '\n')
    return


def receive():
    char = ''
    message = ''
    while char != '\n':
        char = s.recv(1)
        message += char
    return message




def close():
    s.close()
    return


def random_token_generator(size=16, chars=string.ascii_uppercase + string.digits):
    for i in range(size):
        return ''.join(random.choice(chars))


def main():
    userNameList = []
    passwordList = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind(('localhost', 50000))
    server.listen(5)
    while True:
        option = receive()
        option = option.strip('\n')
        if option == '0':
            print("Creating new user")
            write("Registering...")
            username = receive()
            username = username.strip('\n')
            password = receive()
            password = password.strip('\n')
            print(username, password)
            if username in userNameList and password in passwordList and userNameList.index(username) == passwordList.index(password):
                print("Username already in use")
            else:
                userNameList.append(username)
                passwordList.append(password)
                print("User created")
            # Database access
            # cursor = conn.cursor()
            # cursor.execute('insert into usernames (name, password) values (?, ?)', (username, password,))
            # conn.commit()
            # print("Inserted")

        elif option == '1':
            print("Login process")
            print("Logging in...")
            username = receive()
            username = username.strip('\n')
            password = receive()
            password = password.strip('\n')

            # Database access
            # cursor = conn.cursor()
            # cursor.execute('select password from usernames where name = ?', (username,))
            # rows = cursor.fetchall()
            # print rows
            # for row in rows:
            # password_in_db = row
            #password_in_db = userNameList[0]
            #password_in_db = passwordList[0]

            random_token = random_token_generator()
            write(random_token)
            ciphertext = random_token
            #obj = AES.new(random_token, AES.MODE_CBC, 'This is an IV456')
            #ciphertext = obj.encrypt(password)

            read_encrypted_hash = receive()
            # print read_encrypted_hash
            read_encrypted_hash = read_encrypted_hash.strip('\n')

            # print read_encrypted_hash

            if read_encrypted_hash == ciphertext:
                print("Authentication successful!")
                print(read_encrypted_hash, ciphertext)
                write("Successful")
            else:
                print("Password mismatch!")
                write("Wrong Password")
        else:
            pass
        # print("Pass")
        close()
        print("--- New connection ---")


if __name__ == '__main__':
    main()
