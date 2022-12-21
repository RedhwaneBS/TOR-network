#!/bin/env python
from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
import re
# pip install Cryptem
# https://pypi.org/project/Cryptem/


# TODO File Encryption:

# Sender / Encryptor:

crypt = Crypt()  # create Crypt object with new random public and private keys
public_key = crypt.public_key  # read public key

crypt2 = Crypt()  # create Crypt object with new random public and private keys
public_key2 = crypt2.public_key  # read public key

crypt3 = Crypt()  # create Crypt object with new random public and private keys
public_key3 = crypt3.public_key  # read public key


listKeys = [public_key, public_key2, public_key3]
listCrypts = [crypt3, crypt2, crypt]

# TODO Give public_key(the public key) to Sender.

listIP = ['127.0.0.1', '127.0.0.2', '127.0.0.3']

def addHeaderToFile(header,path):
    header = bytes(header, 'utf-8')

    with open(path, 'rb') as file:
        plain_data = file.read()

    encrypted_data = header + plain_data

    with open(path, 'wb') as file:
        file.write(encrypted_data)

    return path

def encryptFileTOR(pathToFile, PathToEncryptedFile, i):
    encryptor = Encryptor(listKeys[i])  # crete Encryptor object with Receiver's public key
    encryptor.EncryptFile(pathToFile, PathToEncryptedFile)  # encrypt a message


#Communication Sender / Encryptor:

path_to_file = ".\\ELECH417_TorProject_2223.pdf"

for i in range(len(listKeys)):
    newPath = ".\\ELECH417_TorProject_2223_" + str(i) + ".pdf"
    path_to_file = addHeaderToFile(listIP[i] + "###", path_to_file)
    encryptFileTOR(path_to_file, newPath, i)
    path_to_file = newPath

# TODO Transmit the encrypted file to Receiver.

def popIP(path):
    ipMatch2 = ""
    with open(path, 'rb') as file:
        plain_data = file.read()
        ipMatch = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', plain_data)  # search for an ip address
        ip = ipMatch.group(0).decode('utf8')  # extract the ip & in string
        ipMatch = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}###', plain_data) # separate the ip address from the payload
        ipMatch2 = ipMatch[1] # keep the payload
    with open('newNewPath.pdf', 'wb') as file:
        file.write(ipMatch2)
    return (ip, 'newNewPath.pdf')


# Communication Receiver:
path_to_encrypted_file = ".\\ELECH417_TorProject_2223_2.pdf"
#path_to_decrypted_file = ".\\ELECH417_TorProject_2223_0.pdf"
#path_to_decrypted_file2 = ".\\ELECH417_TorProject_2223_00.pdf"


for i in range(len(listKeys)):
    j = len(listKeys)-i
    path_to_decrypted_file = ".\\ELECH417_TorProject_2223_" + str(j) + ".pdf"
    listCrypts[i].DecryptFile(path_to_encrypted_file, path_to_decrypted_file)  # decrypt file
    (ip, path_to_encrypted_file) = popIP(path_to_decrypted_file)
    print(ip)

"""
crypt2.DecryptFile(path_to_encrypted_file, path_to_decrypted_file)  # decrypt file
(ip, path_to_decrypted_file) = popIP(path_to_decrypted_file)
print(ip)

crypt.DecryptFile(path_to_decrypted_file, path_to_decrypted_file2)  # decrypt file
(ip, ipMatch) = popIP(path_to_decrypted_file2)
print(ip)
"""

