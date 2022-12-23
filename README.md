# Titre

Authors: 
- Redhwane Ben Salem - redhwane.ben.salem@ulb.be 
- David Touche - david.touche@ulb.be 
- Yen Nhi Nguyen - yen.nhi.nguyen@ulb.be 
- Maxime Pellichero - maxime.pellichero@ulb.be   

Repository for the final project for the "Communication networks : protocols and architectures" course of the ULB. The aim of the project is to design a TOR network and implements it in python .  
The code was tested on Windows and with  python  version 3.10.9 and 3.9.15. 

* * *

## Assumptions
Every client knows the adress and the public key of every other client. 

## How to install
Run this command in a terminal
```python
pip install requirements.txt
```

## How to run the code 
You have to run the nodes first. To run a node open a terminal by node and enter this command:
```
py node.py [ip] [port]
```

Then run the clients with
```
py clients.py [ip] [port] [ip of a node] [port of a node]
```

## How to test 
Run the test.bat or the test.sh (respectively if you are under Windows or Linux) and enter this in the stdin of the client situated on the port 6001  for test: 
```
127.0.0.1//6002 test 
```







