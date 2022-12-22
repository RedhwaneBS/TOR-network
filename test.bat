@echo off

rem Start 2 clients
start cmd /k "python client_manager.py 127.0.0.1 6001"
start cmd /k "python client_manager.py 127.0.0.1 6002"

rem Start 7 Tor nodes
start cmd /k "python node_manager.py 127.0.0.1 6003"
start cmd /k "python node_manager.py 127.0.0.1 6004"
start cmd /k "python node_manager.py 127.0.0.1 6005"
start cmd /k "python node_manager.py 127.0.0.1 6006"
start cmd /k "python node_manager.py 127.0.0.1 6007"
start cmd /k "python node_manager.py 127.0.0.1 6008"
start cmd /k "python node_manager.py 127.0.0.1 6009"

rem enter this in client 1 for test: 127.0.0.1//5002 test 