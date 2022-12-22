#!/bin/bash

echo "" > public_keys.csv

# Start 2 clients
gnome-terminal -- bash -c "python client_manager.py 127.0.0.1 6001"
gnome-terminal -- bash -c "python client_manager.py 127.0.0.1 6002"

# Start 7 Tor nodes
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5003"
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5004"
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5005"
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5006"
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5007"
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5008"
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5009"

# entrer ceci dans le client 1 pour le test : 127.0.0.1//6002 test