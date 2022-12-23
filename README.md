# Titre

Authors: 
- Redhwane Ben Salem - redhwane.ben.salem@ulb.be 
- David Touche - david.touche@ulb.be 
- Yen Nhi Nguyen - yen.nhi.nguyen@ulb.be 
- Maxime Pellichero - maxime.pellichero@ulb.be   

Repository for the final project for the "Communication networks : protocols and architectures" course of the ULB. The aim of the project is to design a TOR network and implements it in python .  
The code was tested on Windows and with  python  version 3.10.9 and 3.9.15. 

* * *
## How to install
Run this command in a terminal
```python
pip install -r requirements.txt
```

## How to test 
Run the test.bat or the test.sh (respectively if you are under Windows or Linux) then wait a few seconds to let the network initialisz himself.

After a certain time you il see :

```
You are registred as : [the name corresponding to your terminal] with the ip : 127.0.0.1 and the port : [your port]
```

Then you can send a message to a terminal via the command line
```
[name] [message]

    exemple :
    YenNhi Hello!
```


## How to run the code manually

You can run a TOR network with :
```
py node_manager.py [ip_node1] [port_node1] [ip_node2] [port_node2] [ip_node3] [port_node3] [ip_node] [port_node4].....
```
You can chose the number of node


Then run a client with
```
py client_manager.py [ip] [port] [ip of the entery node] [port of the entery node]
```
Note that you need an existing node to enter the network






