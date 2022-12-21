import socket
import threading
from Contact import Contact
from Contact_list import Contact_list
from Node import Node

# TCP client that can send and reveive data via a Tor network
class ClientTCP(Node):

    # List of contacts
    contact_list = Contact_list()

    # add a contact to the contact list
    def new_contact(self, tuple_contact):
        new_contact = Contact(
            int(tuple_contact[0]), tuple_contact[1], tuple_contact[2])
        self.contact_list.append(new_contact)
        print(tuple_contact[2] + " has been added to your contacts!")

    # Print the data received
    def manage_data(self, data):
        print(data)


    # Send data to another contact
    def __send_by_contact(self, contact, data):
         self.__send(contact.ip,contact.port,data.encode())


    # Take input to send data to another contact
    def take_input(self):
        while self.run:
            message = input()
            parsed_message = self.__parse_message(message)
            if "//" in parsed_message[0]:
                ip, port = parsed_message[0].split("//")
                self.send_by_ip_port(ip, int(port), parsed_message[1])
            else:
                contact = self.contact_list.find_by_name(parsed_message[0])
                if contact != None:
                    self.__send_by_contact(contact, parsed_message[1])
                else:
                    print("Contact not found")


    # When user enter a message he must do it with the structure "destination_name message"
    # This function parse the message to separate the name of the destination and the message content
    def __parse_message(self, message):
        split_index = message.index(" ")
        splitted_token = message.split(" ")
        return (splitted_token[0], message[split_index + 1:])


