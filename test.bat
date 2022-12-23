@echo off

echo.>public_keys.csv

rem Start a TOR network of 8 nodes
start cmd /k "python node_manager.py 127.0.0.1 5001 127.0.0.1 5002 127.0.0.1 5003 127.0.0.1 5004 127.0.0.1 5005 127.0.0.1 5006 127.0.0.1 5007 127.0.0.1 5008"

rem Start 4 clients
start cmd /k "python client_manager.py 127.0.0.1 6001 127.0.0.1 5001"
start cmd /k "python client_manager.py 127.0.0.1 6002 127.0.0.1 5002"
start cmd /k "python client_manager.py 127.0.0.1 6003 127.0.0.1 5003"
start cmd /k "python client_manager.py 127.0.0.1 6004 127.0.0.1 5004"


