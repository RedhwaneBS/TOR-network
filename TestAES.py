from Crypto.Cipher import AES
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# pip install pycryptodome

#encryption

key = b'Sixteen byte key'

cipher = AES.new(key, AES.MODE_EAX)

data = b'hello'
nonce = cipher.nonce

ciphertext, tag = cipher.encrypt_and_digest(data)



#recipient side

key = b'Sixteen byte key'

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

plaintext = cipher.decrypt(ciphertext)

try:

    cipher.verify(tag)

    print("The message is authentic:", plaintext)

except ValueError:

    print("Key incorrect or message corrupted")