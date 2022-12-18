import hashlib

import rsa
# https://pypi.org/project/rsa/  pip install rsa
# https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files

"""
from diffiehellman import DiffieHellman
#pip install py-diffie-hellman
#https://pypi.org/project/py-diffie-hellman/


hashGen = hashlib.sha256()

# automatically generate two key pairs
dh1 = DiffieHellman(group=14, key_bits=540)
dh2 = DiffieHellman(group=14, key_bits=540)

# get both public keys
dh1_public = dh1.get_public_key()
dh2_public = dh2.get_public_key()

# generate shared key based on the other side's public key
dh1_shared = dh1.generate_shared_key(dh2_public)
dh2_shared = dh2.generate_shared_key(dh1_public)

# the shared keys should be equal
assert dh1_shared == dh2_shared


"""


"""
Load keys from a file
rsa.PrivateKey.load_pkcs1()
rsa.PublicKey.load_pkcs1()
with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
"""

# Create a new pair of keys
(publicKey, privateKey) = rsa.newkeys(512)
(publicKey1, privateKey1) = rsa.newkeys(512)

# Generation of a key pair
# TODO Share the public key.
# RSA -> done such that Alice knows that it is really Bob’s
(A_pub, A_priv) = rsa.newkeys(512)
(B_pub, B_priv) = rsa.newkeys(512)

# Message to be sent, to encode it in UTF-8.\
# The RSA module only operates on bytes, and not on strings.
message = 'Hi Hello!'.encode('utf8')


# Encryption of the message with public key
# TODO Send the encrypted message.

crypto = rsa.encrypt(message, A_pub)
# Reception of the message
# Decryption with private key.
message1 = rsa.decrypt(crypto, A_priv)
print(message1.decode('utf8'))

crypto2 = rsa.encrypt(message, B_pub)
# Reception of the message
# Decryption with private key.
message2 = rsa.decrypt(crypto2, B_priv)
print(message2.decode('utf8'))

if message1 == message2:
    print("ok")
else:
    print('no')

#Since Bob kept his private key private, Alice can be sure that he is the only one who can read the message.\
# Bob does not know for sure that it was Alice that sent the message, since she didn’t sign it.

#RSA can only encrypt messages that are smaller than the key.\
# A couple of bytes are lost on random padding, and the rest is available for the message itself.\
# For example, a 512-bit key can encode a 53-byte message (512 bit = 64 bytes,\
# 11 bytes are used for random padding and other stuff).

