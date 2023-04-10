import sys
import os
import socket
import string
import select

#ip_serv = sys.argv[1]
ip_serv = "192.168.2.4"
#puerto = int(sys.argv[2])
puerto = 1025
address_serv = (ip_serv,puerto)

"""
if(len(sys.argv) != 3):
    print("El numero de parametros pasados no es el correcto\n")
    sys.exit()
"""

if (puerto < 1024 or puerto > 5000):
    print("El puerto que se debe elegir debe estar comprendido en el rango 1024-5000")
    sys.exit()

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Error en la creación del socket.\n")

client_socket.connect(address_serv)

Control_sockets = [sys.stdin, client_socket]

while True:
    print(">>:")
    lectura, _ , _ = select.select(Control_sockets, [],[])

    for s in lectura:
        
        if s == client_socket:
            datos = s.recv(1024)
            if not datos:
                print("Conexion cerrada por el servidor")
                sys.exit()
            else:
                print("<<: ", datos.decode())
        else:
            mensaje = sys.stdin.readline()
            client_socket.send(mensaje.encode())


