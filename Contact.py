from Cryptem import Crypt, Encrypt, Encryptor, EncryptFile
#This class stock the information about a peer that the client want to reach
class Contact:

    #Creation of a new contact
    def __init__(self,port,ip='localhost',name=""):

            self.name = name
            self.ip = ip
            self.port = port
            self.public_key = Crypt().public_key
