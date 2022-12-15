import rsa
# https://pypi.org/project/rsa/  pip install rsa
# https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files

# Create a new pair of keys
(publicKey, privateKey) = rsa.newkeys(512)

"""
Load keys from a file
rsa.PrivateKey.load_pkcs1()
rsa.PublicKey.load_pkcs1()
with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
"""

# Generation of a key pair
# TODO Share the public key.
# RSA -> done such that Alice knows that it is really Bob’s
(bob_pub, bob_priv) = rsa.newkeys(512)

# Message to be sent, to encode it in UTF-8.\
# The RSA module only operates on bytes, and not on strings.
message = 'hello Bob!'.encode('utf8')


# Encryption of the message with public key
# TODO Send the encrypted message.
crypto = rsa.encrypt(message, bob_pub)


# Reception of the message
# Decryption with private key.
message = rsa.decrypt(crypto, bob_priv)
print(message.decode('utf8'))

#Since Bob kept his private key private, Alice can be sure that he is the only one who can read the message.\
# Bob does not know for sure that it was Alice that sent the message, since she didn’t sign it.

#RSA can only encrypt messages that are smaller than the key.\
# A couple of bytes are lost on random padding, and the rest is available for the message itself.\
# For example, a 512-bit key can encode a 53-byte message (512 bit = 64 bytes,\
# 11 bytes are used for random padding and other stuff).
