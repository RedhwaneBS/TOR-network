from Node_TOR import Node_TOR
import sys
import csv
import time
#This fil is used to create the TOR network
#It create nodes and write their coordinates in a csv file
#Then the csv file is used to fill the list of nodes of each node

#Check if the number of arguments is correct
if ((len(sys.argv) - 1) % 2) == 0:

    nodes = []
    datas = []

    #Creat Nodes TOR
    for i in range(1, len(sys.argv) - 1, 2):
        new_node = Node_TOR(sys.argv[i], int(sys.argv[i+1]))
        datas.append([new_node.personal_ip, new_node.personal_port, new_node.crypt.public_key])
        nodes.append(new_node)


    #Write there coordinates in a csv file
    with open('public_keys.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for data in datas:
            writer.writerow(data)

    #Fill the list of nodes of each node
    with open('public_keys.csv', 'r') as fichier_csv:
        # Initialisation du gestionnaire de fichier CSV
        gestionnaire_csv = csv.reader(fichier_csv, delimiter=',')
        # Lecture des lignes du fichier CSV
        for ligne in gestionnaire_csv:
            # Conversion de chaque élément de la ligne en entier (sauf le prénom)
            ligne = [int(x) if x.isdigit() else x for x in ligne]
            # Stockage de la ligne dans un tuple
            tuple_ligne = tuple(ligne)
            if tuple_ligne != ():
                for node in nodes:
                    node.list_of_nodes.append(tuple_ligne)
    print("start")

    #Start the nodes
    for node in nodes:
        node.start()


