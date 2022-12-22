from Node_TOR import Node_TOR
import sys
import csv
import time

ip = sys.argv[1]
port = int(sys.argv[2])

node = Node_TOR(ip, port)

data= [node.personal_ip, node.personal_port, node.crypt.public_key]

with open('data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)

time.sleep(5)

with open('data.csv', 'r') as fichier_csv:
    # Initialisation du gestionnaire de fichier CSV
    gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
    # Lecture des lignes du fichier CSV
    for ligne in gestionnaire_csv:
        # Conversion de chaque élément de la ligne en entier (sauf le prénom)
        ligne = [int(x) if x.isdigit() else x for x in ligne]
        # Stockage de la ligne dans un tuple
        tuple_ligne = tuple(ligne)
        if tuple_ligne != ():
            node.list_of_nodes.append(tuple_ligne)
node.start()


