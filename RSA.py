from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
import re
# pip install Cryptem
# https://pypi.org/project/Cryptem/

list_of_nodes = [("127.0.0.1", 5003), ("127.0.0.1", 5004), ("127.0.0.1", 5005)]

# TODO Single - Session Asymmetric Encryption(public - key and private - key):

#Communication Receiver:
crypt3 = Crypt()  # create Crypt object with new random public and private keys
public_key3 = crypt3.public_key  # read public key

crypt4 = Crypt()  # create Crypt object with new random public and private keys
public_key4 = crypt4.public_key  # read public key

crypt5 = Crypt()  # create Crypt object with new random public and private keys
public_key5 = crypt5.public_key  # read public key

listKeys = [public_key3, public_key4, public_key5]
listCrypts = [crypt5, crypt4, crypt3]

# TODO Give public_key(the public key) to Sender.


#Communication Sender / Encryptor:

def encrypt_the_message(message, i):
    if i == 0:
        message = message.encode('utf-8')
    encryptor = Encryptor(listKeys[i])  # crete Encryptor object with Receiver's public key
    print(list_of_nodes[i][0].encode('utf8') + "//".encode('utf8') + str(list_of_nodes[i][1]).encode('utf8'))
    cipher = encryptor.Encrypt(list_of_nodes[i][0].encode('utf8') + "//".encode('utf8') + str(list_of_nodes[i][1]).encode('utf8') + "###".encode('utf8') + message)  # encrypt a message
    return cipher


message = "Hello there!"
print(message)
for i in range(len(listKeys)):
    message = encrypt_the_message(message, i)
    print(message)


# TODO Transmit cipher to Receiver.

# Communication Receiver:

def pop_IP(plaintext):
    ipMatch = re.search(b'\d{0,9}\.\d{0,9}\.d\{0,9}\.\d{0,9}', plaintext) #search for an ip address
    ip = ipMatch.group(0).decode('utf8') #extract the ip & in string
    ipMatch = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', plaintext) #separate the ip address from the payload
    ipMatch = ipMatch[1] #keep the payload
    return (ip, ipMatch)

def decrypt_the_cipher(crypt, cipher):
    plaintext = crypt.Decrypt(cipher)  # decrypt message
    (ip, ipMatch) = pop_IP(plaintext)
    return (ip, ipMatch)

for i in range(len(listKeys)):
    (ip, message) = decrypt_the_cipher(listCrypts[i], message)
    print(message)
    print(ip)

messageDecrypted = message.decode('utf8')
print(messageDecrypted)



