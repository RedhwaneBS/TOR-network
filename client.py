# the aim of this file is to create a node of a TOR network that can communicate with other nodes

from p2pnetwork.node import Node
from TORClient import TORClient
import sys
import time


# get the arguments from the command line
host = sys.argv[1]
port = int(sys.argv[2])
id = sys.argv[3]

# create a node and start it
node = TORClient(host, port, id)
node.start()


debug = False
node.debug = debug

# connect to the server node

node.connect_with_node("127.0.0.1", 9999)


# ask the user to connect le host and port of the node to connect with
writing_host = input("Give a host to connect to: ")
if writing_host != "None":
    writing_port = int(input("Give a port to connect to: "))
    node.connect_with_node(writing_host, writing_port)


# send a message to the connected nodes
node.send_to_nodes("message: Hi there! I am node " + id)
# node.send_to_node("message: Hi there !",n) #n is the node to send the message to

''' 
    ask the user a message to send to the connected nodes 
    or to reconnect with another node 
    or to stop the node
'''

message = ""
while (message != "exit"):
    if (message == "reconnect"):
        writing_host = input("Give a host to connect to: ")
        writing_port = int(input("Give a port to connect to: "))
        node.connect_with_node(writing_host, writing_port)
        message = ""
    else:
        message = input("Give a message to send: ")
        node.send_to_nodes(message)
        node.send_to_node(message, node.nodes_outbound[0])
print(node.nodes_inbound)
print(node.nodes_outbound)
node.stop()
print("End test")
