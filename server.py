# -*- coding: utf-8 -*-
import sys
import os
from omniORB import CORBA, PortableServer
import CosNaming, Agenda, Agenda__POA
import external_client as ext_clt  

name_server = ext_clt.check()

class Schedule(Agenda__POA.Schedule):
    names = []
    phones = []

    def get_contacts_size(self):
        return len(self.names)

    def get_names(self, index):
        return self.names[index]

    def get_phones(self, index):
        return self.phones[index]

    # Adiciona o contato em si mesmo
    def add(self, name, phone):
        if name not in self.names:
            self.names.append(name)
            self.phones.append(phone)
            self.search()
            print("{} adicionado!".format(name))
        else:
            print("\n ***** Já existe um contato com este nome! *****\n\n")

    # Remove o contato de si mesmo
    def remove(self, index):
        self.search()
        removed = self.names[index]
        del(self.names[index])
        del(self.phones[index])
        self.search()
        print("{} removido!".format(removed))

    # Edita um contato de si mesmo
    def edit(self, index, new_name, new_phone):
        self.names[index] = new_name
        self.phones[index] = new_phone
        self.search()

    # Lista os contatos de si mesmo
    def search(self):
        os.system("clear")
        print("************* Agenda *************")
        for i in range(len(self.names)):         
            print(i, self.names[i], self.phones[i])
        print("**********************************\n")

# Métodos que manipulam os outros servidores agenda 
# (o servidor é cliente das outras agendas)

    def external_add(self, name, phone):
        ext_clt.add(name, phone)             

    def external_remove(self, index):
        ext_clt.remove(index)

    def external_edit(self, index, new_name, new_phone):
        ext_clt.edit(index, new_name, new_phone)

    # Copia os contatos de uma agenda que está online para si mesma
    # Assim quando um agenda cai ela é atualizada por outra que está online
    def receive_backup(self):
        temp_names, temp_phones = ext_clt.backup()
        if temp_names != None:
            self.names, self.phones = temp_names, temp_phones     

    # Este método é invocado para verificar se o servidor está online. Se der 
    # erro ao tentar invocar, uma exceção será levantada e o usuário será 
    # informado que o servidor está offline
    def isOnline(self):
        pass

# Initialise the ORB and find the root POA
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Create an instance of Schedule and an Schedule object reference
ei = Schedule()
eo = ei._this()

# Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print("Failed to narrow the root naming context")
    sys.exit(1)

# Bind context to the root context
try:
    name = [CosNaming.NameComponent(name_server, "context")]
    context = rootContext.bind_new_context(name)
    print("New context bounded: {}".format(name_server))

except CosNaming.NamingContext.AlreadyBound, ex:
    obj = rootContext.resolve(name)
    context = obj._narrow(CosNaming.NamingContext)
    
    if context is None:
        print "context exists but is not a NamingContext"
        sys.exit(1)
    
# Bind the object to the context
try:
    name = [CosNaming.NameComponent("Schedule", "Object")]
    context.bind(name, eo)

except CosNaming.NamingContext.AlreadyBound:
    context.rebind(name, eo)

# Activate the POA
poaManager = poa._get_the_POAManager()
poaManager.activate()

# Recebe os contatos de outra agenda que já estava online
eo.receive_backup()

# Block for ever (or until the ORB is shut down)
orb.run()