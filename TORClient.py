from p2pnetwork.node import Node
from random import randint


class TORClient(Node):

    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(TORClient, self).__init__(
            host, port, id, callback, max_connections)
        self.public_key = ""
        self.BOOMERANGPROBA = 25
        print("MyPeer2PeerNode: Started")

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected (" + self.id + "): " + node.id)

    def inbound_node_connected(self, node):
        print("inbound_node_connected: (" + self.id + "): " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        print("node_message (" + self.id + ") from " + node.id + ": " + str(data))

    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with other outbound node: (" +
              self.id + "): " + node.id)

    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")


    # Boomerang

    def __list_received(self, list):
        if list[0] == "Boomerang":
            self.__boomerangRecieved(list)
        else:
            return list
    
    def __boomerangRecieved(self,list):
        if list[1] == 0:
            # Chose if it launch or not
            if randint(0, 100) < self.BOOMERANGPROBA:
                # Launch
                list[1] = 1
                self.__pass_the_boomerang(list)
            else:
                self.__blur_the_pist(list)
        elif list[1] == 1:
            self.__pass_the_boomerang(list)


    def __pass_the_boomerang(self,list):
        # Check if the boomerang has already reach everyone 2 times
        if list[2] < 2 * (len(list) - 3):
            personal_indice = 2
            # Find his personnal id in the list
            for i in range(2, len(list)):
                if list[i][0] == self.host:
                    list[i][1] = self.public_key
                    personal_indice = i
                    break
            # Set the next indice
            next_indice = personal_indice + 1
            # If the next indice is out of the list bring it back to the first ip of the list
            if next_indice == len(list):
                next_indice = 3

        nextIp = list[next_indice][0]
        # Increment the counter
        list[2] += 1
        # Envoi la liste a nextIP TODO


    # Pass the list to a random member to blur the pist
    def __blur_the_pist(self,list):
        index = randint(3, len(list))
        # Chose a random ip in the list
        ip = list[index][0]
        # Envoi la liste a ip TODO






