from Contact import Contact
from Contact_list import Contact_list
from Client_TOR import Client_TOR
import sys
import csv
import time

ip = sys.argv[1]
port = int(sys.argv[2])

client = Client_TOR(ip, port)
data = [client.personal_ip, client.personal_port, client.crypt.public_key]
"""
with open('public_keys.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)
"""

# Open the file in lecture mode
with open('Contacts.csv', 'r') as fichier_csv:
    # Initialisation of the CSV file manager
    gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
    # Lecture of the lines of the CSV file
    for line in gestionnaire_csv:
        # Convert each element of the line in int (except the name)
        line = [int(x) if x.isdigit() else x for x in line]
        # Put the line in a tuple
        tuple_line = tuple(line)
        client.new_contact(tuple_line)


time.sleep(5)
with open('public_keys.csv', 'r') as fichier_csv:
    # Initialisation of the CSV file manager
    gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
    # Lecture of the lines of the CSV file
    for line in gestionnaire_csv:
        # Convert each element of the line in int (except the name)
        line = [int(x) if x.isdigit() else x for x in line]
        # Put the line in a tuple
        tuple_line = tuple(line)
        if tuple_line != ():
            client.list_of_nodes.append(tuple_line)
print("Welcome to the TOR client! You can now send messages to your contacts.\n "
      "2 options for the required format:\nip//port message\nname message")
client.start()