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
            print("{} is offline :(".format(server))
    for online in online_servers:
        print("{} is ONLINE  :D".format(online))

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

        print("\n***** Conexão estável com o servidor {} *****".format(main_server))
        return obj

    except:
        print("\n ***** O servidor {} está offline, tente novamente *****\n\n".format(main_server))
        return None

def connect():
    onlineServer()
    print("\n*** Escolha o servidor ***")
    print("1 - agenda1")
    print("2 - agenda2")
    print("3 - agenda3")
    try:
        server_name = int(raw_input("\nServidor Selecionado: "))
        if server_name in range(1, 4):
            return names[server_name-1] # retorna "agenda1", "agenda2" ou "agenda3"
    except:
        print("\n***** Este servidor não existe! *****\n *****  Tente novamente *****\n")
        connect()

main_server = connect()

while True:
    print("1 - Adicionar Contato")
    print("2 - Remover Contato")
    print("3 - Editar Contato")
    print("4 - Consultar Agenda")
    print("5 - Limpar tela")

    try:
        option = int(raw_input("Opção: "))    
        eo = bind(main_server)

        if option is 1:
            name  = raw_input("\nNome do contato: ")
            phone = raw_input("Número do contato: ")
            eo.add(name, phone)
            eo.external_add(name, phone)

        elif option is 2:
            if eo.get_contacts_size() == 0:
                print("\n***** A agenda não possui nenhum contato! *****\n\n")
            else:
                eo.search()
                index = int(raw_input("Índice do contato a ser removido: "))
                if index < eo.get_contacts_size():
                    eo.remove(index)
                    eo.external_remove(index)
                else:
                    print("\n***** Este contato não existe! *****\n\n")

        elif option is 3:
            if eo.get_contacts_size() == 0:
                print("\n***** A agenda não possui nenhum contato! *****\n\n")
            else:
                eo.search()
                index = int(raw_input("Índice do contato a ser editado: "))
                if index < eo.get_contacts_size():
                    new_name  = raw_input("Novo nome do contato: ")
                    new_phone = raw_input("Novo número do contato: ")
                    eo.edit(index, new_name, new_phone)
                    eo.external_edit(index, new_name, new_phone)
                else:
                    print("\n***** Este contato não existe *****\n\n")

        elif option is 4:
            eo.search()

        elif option is 5:
            os.system("clear")
        
        else:
            print("\n***** Opção inválida! Tente novamente! ***** \n\n")
    
    except:
        eo = bind(main_server)
        print("\n***** Opção inválida! Tente novamente! ***** \n\n")