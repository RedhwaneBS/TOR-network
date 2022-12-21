import random
import array #TODO changer les listes [ip,NULL] en array pour utiliser moins de mémoire

# List of duos [ip,public key]
# boomerang[1]  is a tag that equal 0 if the boomerang has not been launched and  1 if it has been launch
# boomerang[2] is a count to know were the boomerang is in its travel
#The fisrt element of the list is just "Boomerang" it is here to tel to the client 
# that it is a boomerang list and not just some random data
boomerang = ["Boomerang",0,0,["ip1","NULL"],["ip2","NULL"],["ip3","NULL"],["ip4","NULL"],["ip5","NULL"]]


# Probability that the boomerang is launch in %
BOOMERANGPROBA = 25
personalIp = "ip1"
personalPublicKey = "10354481658"

#When the client receiv a list he check if it is a boomerang list or not
#If it is not a boomerange it just return the list
def listReceived(list):
    if list[0] == "Boomerang":
        boomerangRecieved(list)
    else:
        return list

def boomerangRecieved(list):
    if list[1] == 0:
        # Chose if it launch or not
        if random.randint(0,100) < BOOMERANGPROBA:
            #Launch
            list[1] = 1
            passTheBoomerang(list)
        else:
            blurThePist(list)
    elif list[1] == 1:
        passTheBoomerang(list)

#Pass the list to a random member to blur the pist
def blurThePist(list):
    index = random.randint(3,len(list))
    #Chose a random ip in the list
    ip = list[index][0]
    # Envoi la liste a ip TODO

def passTheBoomerang(list):
    #Check if the boomerang has already reach everyone 2 times
    if list[2] < 2 * (len(list) - 3):
        personalIndice = 2
        #Find his personnal id in the list
        for i in range(2,len(list)):
            if list[i][0] == personalIp:
                list[i][1] = personalPublicKey
                personalIndice = i
                break
        #Set the next indice
        nextIndice = personalIndice + 1
        #If the next indice is out of the list bring it back to the first ip of the list
        if nextIndice == len(list):
            nextIndice = 3
            
        nextIp = list[nextIndice][0]
        # Increment the counter
        list[2] += 1
        # Envoi la liste a nextIP TODO
    
