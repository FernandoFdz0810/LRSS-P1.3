import socket
import sys
import pickle
import select

ip_serv = "192.168.0.37"
#puerto = int(sys.argv[2])
port_serv = 1025
puerto = 0 #El Sist. Operativo asignará un puerto aleatorio disponible para el socket
address_serv = (ip_serv,port_serv)

entradas = [] #Creamos una lista
clientes = {} #Creamos diccionario

# Creación del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexión del socket cliente con el socket servidor
client_socket.connect(address_serv)
data = client_socket.recv(1024) #Recibimos la lista de usuarios del servidor
entradas = pickle.loads(data) #Reconstruir la lista

cl_server_address = ('192.168.0.37', 0)

# Crear un objeto socket, además de comprobar que no ocurren errores en la creación del socket.
try:
    clsocketserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print("Error creando el socket: ", e)

# Configurar el socket para reutilizar la dirección del servidor después de cerrar la conexión.-
clsocketserv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enlazar el objeto socket al host y puerto especificados
try:
    clsocketserv.bind(cl_server_address)
except Exception as e:
    print("Error en la asociación del socket: ", e)

#Conexion con los clientes de la lista

'''
Rellenar
'''

#Añado y coloco el socket en la primera posicion de la lista
entradas.insert(0,clsocketserv)
# Escuchar por conexiones entrantes
clsocketserv.listen(5)

while entradas != -1:

    readable, writable, exceptional = select.select(entradas,[],[])

    for s in readable:
        if s is clsocketserv:
            conexion, client_address = s.accept()
            entradas.append(conexion)
            #clientes[conexion] = client_address
            print("Conexion entrante por parte de {}:{}".format(*client_address))

        else:
            data = s.recv(1024).decode()

            if not data:
            # Si no hay datos entrantes, significa que el cliente cerró la conexión.
                print('Conexión cerrada por {}:{}\n'.format(*client_address))

                #eliminamos el primer elemento de una lista que coincida con el valor s.
                entradas.remove(s)
                #Borramos la entrada correspondiente tambien del diccionario
                if s in clientes:
                    del clientes[s]
                s.close()

            else:
                print("<<: ", data.decode())