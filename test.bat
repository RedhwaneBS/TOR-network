@echo off

start cmd /k "python client.py 127.0.0.1 5001"
start cmd /k "python node_launch.py 127.0.0.1 5002"
start cmd /k "python node_launch.py 127.0.0.1 5003"
start cmd /k "python client.py 127.0.0.1 5004"

rem 127.0.0.1//5002 127.0.0.1//5003 127.0.0.1//5004 test