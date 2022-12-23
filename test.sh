#!/bin/bash

echo "" > public_keys.csv
start cmd /k 


# Start a TOR network of 7 nodes
gnome-terminal -- bash -c "python node_manager.py 127.0.0.1 5001 127.0.0.1 5002 127.0.0.1 5003 127.0.0.1 5004 127.0.0.1 5005 127.0.0.1 5006 127.0.0.1 5007 127.0.0.1 5008"

# Start 4 clients
gnome-terminal -- bash -c "python client_manager.py 127.0.0.1 6001 127.0.0.1 5001"
gnome-terminal -- bash -c "python client_manager.py 127.0.0.1 6002 127.0.0.1 5002"
gnome-terminal -- bash -c "python client_manager.py 127.0.0.1 6003 127.0.0.1 5003"
gnome-terminal -- bash -c "python client_manager.py 127.0.0.1 6004 127.0.0.1 5004"

