# -*- coding: utf-8 -*-
import sys
import os
from omniORB import CORBA, PortableServer
import CosNaming, Agenda, Agenda__POA

names = ["agenda1", "agenda2", "agenda3"]

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Remove da lista o nome da agenda que está chamando as funções
# Assim chamará as funções apenas das outras agendas, e não de si mesma
def check(name_server):
    names.remove(name_server)

# Verifica quais agendas estão online e cria um obj._narrow para cada uma
# Cada servidor agenda cria um obj.narrow apenas para as outras duas agendas
def bind():
    remote_obj = []
    for index, server_name in enumerate(names):
        try:
            obj = orb.resolve_initial_references("NameService")
            rootContext = obj._narrow(CosNaming.NamingContext)
            name = [CosNaming.NameComponent(server_name, "context"),
            CosNaming.NameComponent("Schedule", "Object")]
            
            obj = rootContext.resolve(name)
            obj = obj._narrow(Agenda.Schedule)
            obj.isOnline()
            
            print("{} is up".format(server_name))
            remote_obj.append(obj)

        except:
            print("Servidor {} is down".format(server_name))
    return remote_obj

def add(name, phone):
    remote_obj = bind()
    for index, server_name in enumerate(names):
        # Chama a função add das outras agendas
        remote_obj[index].add(name, phone)

def backup():
    remote_obj = bind()
    print(remote_obj)
    if len(remote_obj) > 0:
        names = []
        phones = []
        contacts_size = remote_obj[0].get_contacts_size()
        for i in range(contacts_size):
            names.append(remote_obj[0].get_names(i))
            phones.append(remote_obj[0].get_phones(i))
        return names, phones
    return None, None
            
def remove(index_name):
    remote_obj = bind()
    for index, server_name in enumerate(names):
        # Chama a função remove das outras agendas
        remote_obj[index].remove(index_name)

def edit(index_name, new_name, new_phone):
    remote_obj = bind()
    for index, server_name in enumerate(names):
        # Chama a função edit das outras agendas
        remote_obj[index].edit(index_name, new_name, new_phone)