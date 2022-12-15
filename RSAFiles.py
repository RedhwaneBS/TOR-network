from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile

# pip install Cryptem
# https://pypi.org/project/Cryptem/

"""
# TODO Single - Session Asymmetric Encryption(public - key and private - key):

#Communication Receiver:
crypt = Crypt()  # create Crypt object with new random public and private keys
public_key = crypt.public_key  # read public key

# TODO Give public_key(the public key) to Sender.

#Communication Sender / Encryptor:
# encryptor = Encryptor(public_key)  # crete Encryptor object with Receiver's public key
# cipher = encryptor.Encrypt("Hello there!".encode('utf-8'))  # encrypt a message


# TODO Transmit cipher to Receiver.

# Communication Receiver:
plaintext = crypt.Decrypt(cipher).decode('utf-8')  # decrypt message
print(plaintext)
"""


# TODO File Encryption:

# RSA encryption rather inefficient with big quantities of data,
# the Crypt and Encryptor classes have functions that implement
# symmetric AES encryption.The secret AES key is encrypted
# with asymmetric elliptic curve cryptography and embedded into the file,
# so that the user can use the file encryption functionality in exactly the same way.

# Sender / Encryptor:

crypt = Crypt()  # create Crypt object with new random public and private keys
public_key = crypt.public_key  # read public key

# TODO Give public_key(the public key) to Sender.

#Communication Sender / Encryptor:
path_to_file = ".\\ELECH417_TorProject_2223.pdf"
path_to_save_encrypted_file = ".\\ELECH417_TorProject_2223_2.pdf"
encryptor = Encryptor(public_key)  # create Encryptor object with Receiver's public key
cipher = encryptor.EncryptFile(path_to_file, path_to_save_encrypted_file)  # encrypt file


# TODO Transmit the encrypted file to Receiver.

# Communication Receiver:
path_to_encrypted_file = ".\\ELECH417_TorProject_2223_2.pdf"
path_to_decrypted_file = ".\\ELECH417_TorProject_2223_3.pdf"
plaintext = crypt.DecryptFile(path_to_encrypted_file, path_to_decrypted_file)  # decrypt file

