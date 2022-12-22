from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
import re
# pip install Cryptem
# https://pypi.org/project/Cryptem/



# TODO Single - Session Asymmetric Encryption(public - key and private - key):

#Communication Receiver:

# TODO Give public_key(the public key) to Sender.


#Communication Sender / Encryptor:

def encrypt_the_message(message, node):
    if isinstance(message, str):
        message = message.encode('utf-8')
    encryptor = Encryptor(node[2])  # crete Encryptor object with Receiver's public key
    cipher = encryptor.Encrypt(message)  # encrypt a message
    return cipher




# TODO Transmit cipher to Receiver.

# Communication Receiver:

def pop_header(plaintext):
    headerInPlaintext = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9}', plaintext)  # search for a header
    header = headerInPlaintext.group(0)  # extract the header
    searchIP = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', header)
    ip = searchIP.group(0)  # extract the header
    port = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//', header)
    port = port[1]  # extract the header
    splitHeaderPlaintext = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', plaintext, 1)  # separate the header from the payload
    restPlaintext = splitHeaderPlaintext[1]  # keep the payload
    return (ip, port, restPlaintext)

def decrypt_the_cipher(crypt, cipher):
    plaintext = crypt.Decrypt(cipher)  # decrypt message
    return plaintext



