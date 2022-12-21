import Contact

#The purpose of this class is to make actions on the contact list easyer
class Contact_list:


    #Constructor 
    def __init__(self,contact_lsit=None):
        if contact_lsit == None:
            self.contacts = []
        else:
            self.contacts = contact_lsit

    #Add a copntact to the lsit
    def append(self,contact):
        self.contacts.append(contact)

    #remove a contact
    def remove(self,contact):   
        self.contacts.remove(contact)

    #remove a contact
    def remove_by_ip(self,ip):
        contact = self.find_by_ip(ip)  
        self.contacts.remove(contact)

    #remove a contact
    def remove_by_name(self,name):
        contact = self.find_by_name(name)
        self.contacts.remove(contact)

    #Find a contact by its name in the list
    def find_by_name(self,name):
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

    #Find a contact by its ip in the list
    def find_by_ip(self,ip):
        for contact in self.contacts:
            if contact.ip == ip:
                return contact
        return None

    #Find a contact by its ip in the list
    def find_by_ip_port(self,ip,port):
        for contact in self.contacts:
            if contact.ip == ip and contact.port == port:
                return contact
        return None
