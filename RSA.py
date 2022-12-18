from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
# pip install Cryptem
# https://pypi.org/project/Cryptem/


# TODO Single - Session Asymmetric Encryption(public - key and private - key):

#Communication Receiver:
crypt = Crypt()  # create Crypt object with new random public and private keys
public_key = crypt.public_key  # read public key

crypt2 = Crypt()  # create Crypt object with new random public and private keys
public_key2 = crypt2.public_key  # read public key

# TODO Give public_key(the public key) to Sender.

#Communication Sender / Encryptor:
encryptor = Encryptor(public_key)  # crete Encryptor object with Receiver's public key
cipher = encryptor.Encrypt("Hello there!".encode('utf-8'))  # encrypt a message

encryptor2 = Encryptor(public_key2)  # crete Encryptor object with Receiver's public key
cipher2 = encryptor2.Encrypt(cipher)  # encrypt a message


# TODO Transmit cipher to Receiver.

# Communication Receiver:
plaintext2 = crypt2.Decrypt(cipher2)  # decrypt message
plaintext = crypt.Decrypt(cipher).decode('utf-8')  # decrypt message

print(plaintext)










