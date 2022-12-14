import rsa
# https://pypi.org/project/rsa/  pip install rsa

# Create a new pair of keys
(pubkey, privkey) = rsa.newkeys(512)

print(pubkey)
print(privkey)


"""
Load keys from a file
rsa.PrivateKey.load_pkcs1()
rsa.PublicKey.load_pkcs1()
with open('private.pem', mode='rb') as privatefile:
    keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
"""
#############

# https://stuvel.eu/python-rsa-doc/usage.html#working-with-big-files

# Bob generates a key pair, and gives the public key to Alice. \
# This is done such that Alice knows for sure that the key is really Bob’s
(bob_pub, bob_priv) = rsa.newkeys(512)

# Alice writes a message, and encodes it in UTF-8.\
# The RSA module only operates on bytes, and not on strings, so this step is necessary.
message = 'hello Bob!'.encode('utf8')
#message = jetbrains://pycharm/navigate/reference?project=TOR-network&path=



#@Alice encrypts the message using Bob’s public key, and sends the encrypted message.
crypto = rsa.encrypt(message, bob_pub)
print('message encrypté')
print(crypto)

#Bob receives the message, and decrypts it with his private key.
message = rsa.decrypt(crypto, bob_priv)
print('message décrypté')
print(message.decode('utf8'))

#Since Bob kept his private key private, Alice can be sure that he is the only one who can read the message.\
# Bob does not know for sure that it was Alice that sent the message, since she didn’t sign it.

#RSA can only encrypt messages that are smaller than the key.\
# A couple of bytes are lost on random padding, and the rest is available for the message itself.\
# For example, a 512-bit key can encode a 53-byte message (512 bit = 64 bytes,\
# 11 bytes are used for random padding and other stuff).

################## Signature
# with open('somefile', 'rb') as msgfile:
#     signature = rsa.sign(msgfile, privkey, 'SHA-1')
#
# with open('somefile', 'rb') as msgfile:
#     rsa.verify(msgfile, signature, pubkey)
