@echo off

echo.>public_keys.csv

rem Start 2 clients
start cmd /k "python client_manager.py 127.0.0.1 5001"
start cmd /k "python client_manager.py 127.0.0.1 5002"

rem Start 7 Tor nodes
start cmd /k "python node_manager.py 127.0.0.1 5003"
start cmd /k "python node_manager.py 127.0.0.1 5004"
start cmd /k "python node_manager.py 127.0.0.1 5005"
start cmd /k "python node_manager.py 127.0.0.1 5006"
start cmd /k "python node_manager.py 127.0.0.1 5007"
start cmd /k "python node_manager.py 127.0.0.1 5008"
start cmd /k "python node_manager.py 127.0.0.1 5009"

rem enter this in client 1 for test: 127.0.0.1//5002 test
