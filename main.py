import subprocess
import sys
import time

#le but du main est de lancer 2 noeuds et 2 clients
#le client 1 va envoyer un message au client 2 en passant par les 2 noeuds
#le client 1 se trouve à l'adresse 127.0.0.1 et au port 5001
#le noeud 1 se trouve à l'adresse 127.0.0.1 et au port 5002
#le noeud 2 se trouve à l'adresse 127.0.0.1 et au port 5003
#le client 2 se trouve à l'adresse 127.0.0.1 et au port 5004

#dans la liste files_and_args, on met les fichiers à lancer et leurs arguments
files_and_args = [("client.py",("127.0.0.1", "5001")),
                  ("node.py",("127.0.0.1", "5002")),
                  ("node.py",("127.0.0.1", "5003")),
                  ("client.py",("127.0.0.1", "5004"))]

#on lance les fichiers dans la liste files_and_args avec leurs arguments respectifs dans des processus séparés
subprocesses=[]
for file, args in files_and_args:
    subprocesses.append(subprocess.Popen([sys.executable, file, args[0], args[1]],stdin=subprocess.PIPE, stdout=subprocess.PIPE))


#on attend 5 secondes pour que les processus se lancent
time.sleep(5)

#on envoie un message du client 1 au client 2
message="127.0.0.1//5002 127.0.0.1//5003 127.0.0.1//5004 test"
input_str = "Entrée pour le script1\n"
subprocesses[0].stdin.write(input_str.encode())
subprocesses[0].stdin.flush()
