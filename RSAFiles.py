from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
# pip install Cryptem
# https://pypi.org/project/Cryptem/


# TODO File Encryption:

# RSA encryption rather inefficient with big quantities of data,
# the Crypt and Encryptor classes have functions that implement
# symmetric AES encryption.The secret AES key is encrypted
# with asymmetric elliptic curve cryptography and embedded into the file,
# so that the user can use the file encryption functionality in exactly the same way.

# Sender / Encryptor:

crypt = Crypt()  # create Crypt object with new random public and private keys
public_key = crypt.public_key  # read public key

crypt2 = Crypt()  # create Crypt object with new random public and private keys
public_key2 = crypt2.public_key  # read public key


# TODO Give public_key(the public key) to Sender.
"""
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

"""
#Communication Sender / Encryptor:
path_to_file = ".\\ELECH417_TorProject_2223.pdf"
path_to_save_encrypted_file = ".\\ELECH417_TorProject_2223_2.pdf"
path_to_save_encrypted_file2 = ".\\ELECH417_TorProject_2223_25.pdf"
encryptor = Encryptor(public_key)  # create Encryptor object with Receiver's public key
encryptor2 = Encryptor(public_key2)  # create Encryptor object with Receiver's public key
cipher = encryptor.EncryptFile(path_to_file, path_to_save_encrypted_file)  # encrypt file
cipher2 = encryptor2.EncryptFile(path_to_save_encrypted_file, path_to_save_encrypted_file2)  # encrypt file


# TODO Transmit the encrypted file to Receiver.

# Communication Receiver:
path_to_encrypted_file = ".\\ELECH417_TorProject_2223_25.pdf"
path_to_decrypted_file = ".\\ELECH417_TorProject_2223_3.pdf"
path_to_decrypted_file2 = ".\\ELECH417_TorProject_2223_4.pdf"
plaintext = crypt2.DecryptFile(path_to_encrypted_file, path_to_decrypted_file)  # decrypt file
plaintext2 = crypt.DecryptFile(path_to_decrypted_file, path_to_decrypted_file2)  # decrypt file

