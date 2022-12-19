from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
import re
# pip install Cryptem
# https://pypi.org/project/Cryptem/

listIP = ['127.0.0.1', '127.0.0.2', '127.0.0.3']


# TODO Single - Session Asymmetric Encryption(public - key and private - key):

#Communication Receiver:
crypt = Crypt()  # create Crypt object with new random public and private keys
public_key = crypt.public_key  # read public key

crypt2 = Crypt()  # create Crypt object with new random public and private keys
public_key2 = crypt2.public_key  # read public key

crypt3 = Crypt()  # create Crypt object with new random public and private keys
public_key3 = crypt3.public_key  # read public key

listKeys = [public_key, public_key2, public_key3]
listCrypts = [crypt3, crypt2, crypt]

# TODO Give public_key(the public key) to Sender.


#Communication Sender / Encryptor:

def encryptTheMessage(message, i):
    if i == 0:
        message = message.encode('utf-8')
    encryptor = Encryptor(listKeys[i])  # crete Encryptor object with Receiver's public key
    cipher = encryptor.Encrypt(listIP[i].encode('utf8') +"###".encode('utf8')+ message)  # encrypt a message
    return cipher


message = "Hello there!"
for i in range(len(listKeys)):
    message = encryptTheMessage(message, i)


# TODO Transmit cipher to Receiver.

# Communication Receiver:

def popIP(plaintext):
    ipMatch = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', plaintext) #search for an ip address
    ip = ipMatch.group(0).decode('utf8') #extract the ip & in string
    ipMatch = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}###', plaintext) #separate the ip address from the payload
    ipMatch = ipMatch[1] #keep the payload
    return (ip, ipMatch)

def decryptTheCipher(crypt, cipher):
    plaintext = crypt.Decrypt(cipher)  # decrypt message
    (ip, ipMatch) = popIP(plaintext)
    return (ip, ipMatch)

for i in range(len(listKeys)):
    (ip, message) = decryptTheCipher(listCrypts[i], message)
    print(ip)

messageDecrypted = message.decode('utf8')
print(messageDecrypted)



