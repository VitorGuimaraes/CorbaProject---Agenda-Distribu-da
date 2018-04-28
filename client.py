# -*- coding: utf-8 -*-
import os
import sys
from omniORB import CORBA, PortableServer
import CosNaming, Agenda, Agenda__POA
import time

names = ["agenda1", "agenda2", "agenda3"]

# Initialise the ORB
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

#Informa os servidores que estão online
def onlineServer():
    online_servers = []
    for server in names:
        try:
            obj = orb.resolve_initial_references("NameService")
            rootContext = obj._narrow(CosNaming.NamingContext)

            name = [CosNaming.NameComponent(server, "context"),
            CosNaming.NameComponent("Schedule", "Object")]
            
            obj = rootContext.resolve(name)
            object_remote = obj._narrow(Agenda.Schedule)
            object_remote.isOnline()
            online_servers.append(server)

        except:
            print("Server {} is offline :(".format(server))
    for online in online_servers:
        print("Server {} is ONLINE  :D".format(online))

# Conecta a um servidor 
def bind(main_server):
    try:    
        obj = orb.resolve_initial_references("NameService")
        rootContext = obj._narrow(CosNaming.NamingContext)
    
        name = [CosNaming.NameComponent(main_server, "context"),
        CosNaming.NameComponent("Schedule", "Object")]
    
        obj = rootContext.resolve(name)
        obj = obj._narrow(Agenda.Schedule)
        obj.isOnline()

        print("\nConectado ao servidor {}".format(main_server))
        # Narrow the object to an Agenda::Schedule
        return obj

    except:
        print("\n\nO servidor {} caiu, tente novamente".format(main_server))
        return None

def connect():
    onlineServer()
    server_name = raw_input("\nServidor escolhido: ")
    return server_name

main_server = connect()

while True:
    print("1 - Adicionar Contato")
    print("2 - Remover Contato")
    print("3 - Editar Contato")
    print("4 - Consultar Agenda")
    print("5 - Limpar tela")

    option = int(raw_input("Opção: "))    
    eo = bind(main_server)

    if eo is None:
        main_server = connect()
        eo = bind(main_server)

    if option is 1:
        name  = raw_input("\nNome do contato: ")
        phone = raw_input("Número do contato: ")
        eo.add(name, phone)
        eo.external_add(name, phone)

    elif option is 2:
        eo.search()
        index = int(raw_input("Índice do contato a ser removido: "))
        eo.remove(index)
        eo.external_remove(index)

    elif option is 3:
        eo.search()
        index     = int(raw_input("Índice do contato a ser editado: "))
        new_name  = raw_input("Novo nome do contato: ")
        new_phone = raw_input("Novo número do contato: ")
        eo.edit(index, new_name, new_phone)
        eo.external_edit(index, new_name, new_phone)

    elif option is 4:
        eo.search()

    elif option is 5:
        os.system("clear")
    
    else:
        print("Opção inválida! Tente novamente!\n")