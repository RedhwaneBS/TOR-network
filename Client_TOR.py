import socket
import threading
import random
from Contact import Contact
from Contact_list import Contact_list
from Element import Element


# TCP client that can send and reveive data via a Tor network
class Client_TOR(Element):

    # List of contacts
    contact_list = Contact_list()
    # List of nodes coordinates
    list_of_nodes = [("127.0.0.1", 5003), ("127.0.0.1", 5004), ("127.0.0.1", 5005), ("127.0.0.1", 5006), ("127.0.0.1", 5007), ("127.0.0.1", 5008), ("127.0.0.1", 5009)]

    # Creat a message with a path of nodes
    def create_message(self, path, message):
        nodes_string = ""
        for node in path:
            print(nodes_string)
            nodes_string += f"{node[0]}//{node[1]} "
        nodes_string+=message
        print(nodes_string)
        return nodes_string

    # Return a random list of node to create a path
    def randomiser(self, liste):
        # tire un nombre au hasard entre 0 et la longueur de la liste
        nombre = random.randint(1, len(liste) - 1)

        # retourne ce nombre d'éléments de la liste
        new_liste = random.sample(liste, nombre)
        return new_liste

    # add a contact to the contact list
    def new_contact(self, tuple_contact):
        new_contact = Contact(int(tuple_contact[0]), tuple_contact[1], tuple_contact[2])
        self.contact_list.append(new_contact)
        print(tuple_contact[2] + " has been added to your contacts!")


    # Print the data received
    def manage_data(self, data):
        print(data)


    # Parse the input to send data to another contact
    def take_input(self):

        while self.run:
            head_type = 0
            send_message = False
            message = input()
            head,data = self.__parse_message(message)
            head_parsed = head.split("//")
            if head_parsed != None:
                head_type = len(head_parsed)

            if head_type == 1:
                if head in self.contact_list.get_list_of_names():
                    contact = self.contact_list.get_contact_by_name(head)
                    message = f"{contact.ip}//{contact.port} "  + data
                    send_message = True

                elif head == "add":
                    tuple_contact = data.split(" ")
                    self.new_contact(tuple_contact)

                else:
                    print(head + " is not in your contact list or is an ivalid input") 
                    print("Please enter a valid input or add the contact to your contact list using the command 'add' [port] [ip] [name]")
            elif head_type != 2:
                print("Invalid input header")
                print("Please enter an input following the scheme ip//port message or contact_name message")
                print("You can add a contact to your contact list using the command 'add' [port] [ip] [name]")
            elif head_type == 2:
                send_message = True

            if send_message:
                message_with_path_header = self.create_message((self.list_of_nodes), message)
                print(message_with_path_header)
                parsed_message = self.__parse_message(message_with_path_header)
                ip, port = parsed_message[0].split("//")
                self.send(ip, int(port), parsed_message[1])
            

    # When user enter a message he must do it with the structure "destination_name message"
    # This function parse the message to separate the name of the destination and the message content
    def __parse_message(self, message):
        split_index = message.index(" ")
        splitted_token = message.split(" ")
        return (splitted_token[0], message[split_index + 1:])


