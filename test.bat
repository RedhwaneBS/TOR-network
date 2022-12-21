@echo off

start cmd /k "python client.py 127.0.0.1 5001"
start cmd /k "python node.py 127.0.0.1 5002"
start cmd /k "python node.py 127.0.0.1 5003"
start cmd /k "python client.py 127.0.0.1 5004"