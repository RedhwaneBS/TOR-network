#!/usr/bin/env python
import socket, time
import getpass
import hashlib

from Crypto.Cipher import AES


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
    return 'my password'
    user_in = getpass.getpass()
    password = hashlib.md5()
    password.update(user_in.encode("utf-8"))
    return password.hexdigest()


def main():
    connect('127.0.0.1', 17093)
    print(receive())
    username = input("Enter your username: ")
    write(username)
    password = PasswordCreate()
    print("Password: " + password)
    write(password)
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
            random_token = receive()
            random_token = random_token.strip('\n')
            print("Random token: ", random_token)
            ciphertext = random_token
            obj = AES.new(random_token, AES.MODE_CBC, 'This is an IV456')
            ciphertext = obj.encrypt(password)
            write(ciphertext)
            print('cipher sent')
            auth_stat = receive()
            auth_stat = auth_stat.strip('\n')
            print('auth_stat :', auth_stat)

    close()


if __name__ == '__main__':
    while True :
        print("--- New connection ---")
        main()
