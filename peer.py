import socket
import sys

IP = '172.22.58.104'
PUERTO = 1029

# Creación del socket
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conexión del socket cliente con el socket servidor


# 1º Parte: Solicitud al servidor de la lista de clientes que tiene asociada
peer_socket.connect((IP, PUERTO))
print("Introduce tú nombre de usuario: ")
n_usuario = input()
Añadir_Usuario = "add_user " + n_usuario 
peer_socket.send(Añadir_Usuario.encode())

Respuesta_añadir_user = peer_socket.recv(1024)

print(Respuesta_añadir_user.decode())

Solicitar_Usuarios = "get_users"
peer_socket.send(Solicitar_Usuarios.encode())

Usuarios_existentes = peer_socket.recv(1024)

Tamaño_Lista_Usuarios = len(Usuarios_existentes)
if Tamaño_Lista_Usuarios == 0:
    print("No existen usuarios en la lista.")
else:
   print("El numero de usuarios en el servidor es el siguiente: ".format(Usuarios_existentes))


