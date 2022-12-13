#the aim of this file is to create a node of a TOR network that can communicate with other nodes

from p2pnetwork.node import Node
from myTORNode import myTORNode
import sys
import time

host = sys.argv[1]
port = int(sys.argv[2])
id = sys.argv[3]

node = myTORNode(host, port, id)

node.start()

debug = False
node.debug = debug

writing_host = input("Give a host to connect to: ")
if writing_host != "None":
    writing_port = int(input("Give a port to connect to: "))
    node.connect_with_node(writing_host, writing_port)

time.sleep(10)
node.send_to_nodes("message: Hi there! I am node " + id)
#node.send_to_node("message: Hi there !",n) #n is the node to send the message to

message = ""
while(message != "exit"):
    if(message == "reconnect"):
        writing_host = input("Give a host to connect to: ")
        writing_port = int(input("Give a port to connect to: "))
        node.connect_with_node(writing_host, writing_port)
        message = ""
    else:
        message = input("Give a message to send: ")
        node.send_to_nodes(message)


print("End test")

