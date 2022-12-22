import re

def pop_header(plaintext):
    headerInPlaintext = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9}', plaintext) #search for a header
    header = headerInPlaintext.group(0) #extract the header
    searchIP = re.search(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', header)
    ip = searchIP.group(0)  # extract the header
    port = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//', header)
    port = port[1]  # extract the header
    splitHeaderPlaintext = re.split(b'\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}//\d{0,9} ', plaintext, 1) #separate the header from the payload
    restPlaintext = splitHeaderPlaintext[1] #keep the payload
    return (ip, port, restPlaintext)

plaintext = b'127.0.0.1//5004 127.0.0.1//5005 Message'

(header, header2, restPlaintext) = pop_header(plaintext)
print(header.decode('utf8'))
print(header2.decode('utf8'))
print(restPlaintext.decode('utf8'))



