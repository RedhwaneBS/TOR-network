from p2pnetwork.node import Node


class TORServer(Node):

    def __init__(self, callback=None, max_connections=0):
        super(TORServer, self).__init__("127.0.0.1", 9999, "server", callback, max_connections)
        print("TORServer: Started")

    def node_message(self, node, data):
        print("client: (" + self.id + ") from " + node.id + ": " + str(data))
        print("client: (" + self.id + "): " + node.id + " sent " + data)

    ##when a  new node is connected send the list of nodes to the new node
    def outbound_node_connected(self, node):
        print("client: (" + self.id + "): " + node.id + " connected")
        for i in range(len(self.nodes_outbound)):
            self.send_to_nodes("list: " + str(self.nodes_outbound[i]))

    def inbound_node_connected(self, node):
        print("client: (" + self.id + "): " + node.id + " connected")
        for i in range(len(self.nodes_inbound)):
            self.send_to_nodes("list: " + str(self.nodes_inbound[i]))

    def inbound_node_disconnected(self, node):
        print("client: (" + self.id + "): " + node.id + " disconnected")

    def outbound_node_disconnected(self, node):
        print("client: (" + self.id + "): " + node.id + " disconnected")

