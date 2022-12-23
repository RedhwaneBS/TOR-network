from Contact import Contact
from Contact_list import Contact_list
from Client_TOR import Client_TOR
import sys
import csv
import time

ip = sys.argv[1]
port = int(sys.argv[2])
connexion_ip = sys.argv[3]
connexion_port = int(sys.argv[4])

client = Client_TOR(ip, port, connexion_ip, connexion_port)
data = [client.personal_ip, client.personal_port, client.crypt.public_key]

# Ouverture du fichier en mode lecture
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

time.sleep(10)

print("Welcome to the TOR client! You can now send messages to your contacts.")
client.start()