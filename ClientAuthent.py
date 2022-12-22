#!/usr/bin/env python
import os
import socket, time
import getpass
import hashlib

from Crypto.Cipher import AES
import rsa


def connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return


def write(message):
    s.send((message + '\n').encode())
    return


def receive():
    char = ''
    message = ''
    while char != '\n':
        char = (s.recv(1)).decode()
        message += char
    return message


def close():
    s.close()
    return


def PasswordCreate():
    random_key = os.urandom(16)
    return random_key

def main():
    connect('127.0.0.1', 17092)
    print(receive())
    username = input("Enter your username: ")
    write(username)
    if username in UsernameList:
        print("Username already exists")
        index = UsernameList.index(username)
        password = PasswordList[index]
    else:
        password = PasswordCreate()
        UsernameList.append(username)
        PasswordList.append(password)

    print("Password: ", password)
    s.send(password)
    print(receive())
    option = input('Type 1 for login or 0 for register: ')
    write(option)
    if option == '0':
        print('Registration sent')
    elif option == '1':
        existence = receive()
        existence = existence.strip('\n')
        print('Existence :', existence)
        false = '1'
        if existence == false:
            print("Username or password is incorrect")
            close()
        else:
            # Ancienne partie token
            random_token = s.recv(1024)
            print("Random token :", random_token)
            print("password : ", password)
            nonce = s.recv(1024)
            obj = AES.new(random_token, AES.MODE_EAX, nonce=nonce)
            ciphertext, tag = obj.encrypt_and_digest(password)

            # Envoi du token chiffré
            s.send(ciphertext)
            print('cipher sent : ', ciphertext)
            auth_stat = receive()
            auth_stat = auth_stat.strip('\n')
            print('auth_stat :', auth_stat)

    close()


if __name__ == '__main__':

    UsernameList = []
    PasswordList = []
    while True:
        print("--- New connection ---")
        main()
