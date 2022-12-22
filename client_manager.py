from Contact import Contact
from Contact_list import Contact_list
from Client_TOR import Client_TOR
import sys
import csv
import time

ip = sys.argv[1]
port = int(sys.argv[2])

client = Client_TOR(ip, port)

# Ouverture du fichier en mode lecture
with open('Contacts.csv', 'r') as fichier_csv:
    # Initialisation du gestionnaire de fichier CSV
    gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
    # Lecture des lignes du fichier CSV
    for ligne in gestionnaire_csv:
        # Conversion de chaque élément de la ligne en entier (sauf le prénom)
        ligne = [int(x) if x.isdigit() else x for x in ligne]
        # Stockage de la ligne dans un tuple
        tuple_ligne = tuple(ligne)
        client.new_contact(tuple_ligne)

time.sleep(10)

with open('data.csv', 'r') as fichier_csv:
    # Initialisation du gestionnaire de fichier CSV
    gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
    # Lecture des lignes du fichier CSV
    for ligne in gestionnaire_csv:
        # Conversion de chaque élément de la ligne en entier (sauf le prénom)
        ligne = [int(x) if x.isdigit() else x for x in ligne]
        # Stockage de la ligne dans un tuple
        tuple_ligne = tuple(ligne)
        print(tuple_ligne)
        client.list_of_nodes.append(tuple_ligne)


client.start()


