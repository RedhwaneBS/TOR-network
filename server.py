from p2pnetwork.node import Node
from TORServer import TORServer
import time

host = "127.0.0.1"
port = 9999
id = "server"

node = TORServer()
node.start()


debug = False
node.debug = debug
print("TORServer: Started")
print("TORServer: Waiting for connections")
print("press CTRL+C to stop")
try:
    while True:
        time.sleep(1)
        node.send_to_node("message: Hi there !", node.nodes_outbound[0])
except KeyboardInterrupt:
    print('interrupted!')

node.stop()
