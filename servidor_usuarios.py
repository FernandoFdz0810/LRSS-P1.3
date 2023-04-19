import sys
import os
import socket
import queue
import select 
import pickle

"""
puerto = int(sys.argv[1])
if (puerto < 1024 or puerto > 5000):
    print("El puerto que se debe elegir debe estar comprendido en el rango 1024-5000")
    sys.exit()
"""

# Establecer el host y el puerto del servidor
server_address = ('192.168.0.37', 1025)

# Crear un objeto socket, además de comprobar que no ocurren errores en la creación del socket.
try:
    socketserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except Exception as e:
    print("Error creando el socket: ", e)

# Configurar el socket para reutilizar la dirección del servidor después de cerrar la conexión.-
socketserv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enlazar el objeto socket al host y puerto especificados
try:
    socketserv.bind(server_address)
except Exception as e:
    print("Error en la asociación del socket: ", e)

# Escuchar por conexiones entrantes
socketserv.listen(5)

entradas = [socketserv]
clientes = {}

while entradas != -1:
    print("Esperando peticiones entrantes...\n")

    readable, writable, exceptional = select.select(entradas,[],[])

    for s in readable:
        if s is socketserv:
            conexion, client_address = s.accept()
            entradas.append(conexion)
            clientes[conexion] = client_address
            print("Conexion entrante por parte de {}:{}".format(*client_address))
            '''
            # pickle.dumps(entradas) convierte la lista de usuarios "entradas" en un objeto de bytes de Python, 
            utilizando el módulo "pickle". Esto permite enviar la lista de usuarios a través de la red,
            ya que los objetos de bytes pueden ser transmitidos y reconstruidos en otro lugar.'''
            
            usuarios = pickle.dumps(entradas) 
            conexion.send(usuarios) #Enviar la lista al cliente nuevo

            
        else:
            data = s.recv(1024).decode()

            if not data:
            # Si no hay datos entrantes, significa que el cliente cerró la conexión.
                print('Conexión cerrada por {}:{}\n'.format(*client_address))
            # En ese caso, se saca al cliente de la lista de entradas y, se cierra el socket.
                #eliminamos el primer elemento de una lista que coincida con el valor s.
                entradas.remove(s)
                #Borramos la entrada correspondiente tambien del diccionario
                if s in clientes:
                    del clientes[s]
                s.close()
                # Aqui solo actualizamos la lista para que desaparezca de la lista el cliente desconectado
            '''
            else:
                for conexion in clientes:
                    if conexion != server_address and conexion != s:
                        print("Mensaje enviado por el cliente {}".format(clientes[conexion]))
                        Info = "Mensaje enviado por el cliente {}: ".format(clientes[conexion])
                        Datos = Info + data
                        conexion.send(Datos.encode())
                        '''