<<<<<<< HEAD:client_manager.py
from Contact import Contact
from Contact_list import Contact_list
from Client_TOR import ClientTCP
import sys
import csv
=======
from Node_TOR import Node_TOR
import sys
import csv
import time
>>>>>>> main:node_manager.py

ip = sys.argv[1]
port = int(sys.argv[2])

<<<<<<< HEAD:client_manager.py
client = ClientTCP(ip, port)
client.start()


# Ouverture du fichier en mode lecture
with open('Contacts.csv', 'r') as fichier_csv:
=======
node = Node_TOR(ip, port)

data = [node.personal_ip, node.personal_port, node.crypt.public_key]

with open('public_keys.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)

time.sleep(5)

with open('public_keys.csv', 'r') as fichier_csv:
>>>>>>> main:node_manager.py
    # Initialisation du gestionnaire de fichier CSV
    gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
    # Lecture des lignes du fichier CSV
    for ligne in gestionnaire_csv:
        # Conversion de chaque élément de la ligne en entier (sauf le prénom)
        ligne = [int(x) if x.isdigit() else x for x in ligne]
        # Stockage de la ligne dans un tuple
        tuple_ligne = tuple(ligne)
<<<<<<< HEAD:client_manager.py
        client.new_contact(tuple_ligne)
=======
        if tuple_ligne != ():
            node.list_of_nodes.append(tuple_ligne)
node.start()


>>>>>>> main:node_manager.py
