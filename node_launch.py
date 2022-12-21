from Node_TOR import Node_TOR
import sys

ip = sys.argv[1]
port = int(sys.argv[2])

client = Node_TOR(ip, port)
client.start()
