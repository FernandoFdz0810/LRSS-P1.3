import socket
import sys
import pickle

# Definir la dirección IP y el puerto de escucha del servidor

"""
sys.argv[1] = IP
sys.argv[2] = PORT
"""

IP = '172.22.58.104'
PORT = 1029


# Crear un socket para el servidor y establecer la conexión
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asociacion de dirección IP y Servidor al socket servidor
server_socket.bind((IP, PORT))
server_socket.listen(1)

# Lista de usuarios
users = []

while True:

    # Aceptar una conexión entrante del cliente
    connection, address = server_socket.accept()
    print("Conexión establecida con", address)
    request = connection.recv(1024).decode()
    # Recibir la solicitud del cliente
    while request != -1:

        print(request)

            # Si el cliente solicita la lista de usuarios, enviarla
        if request == "get_users":
                #user_list = ",".join(users)
            usuarios = pickle.dumps(users)
            connection.send(usuarios)
            # Si el cliente intenta agregar un usuario a la lista, agregarlo
        elif request.startswith("add_user"):
            new_user = request.split(" ")[1]
            puerto = str(address[1])
            añadir = new_user + ' ' + puerto
            users.append(añadir)
                
            connection.send("Usuario agregado con éxito".encode())

        request = connection.recv(1024).decode()

    # Cerrar la conexión con el cliente
    connection.close()

# Cerrar el socket del servidor
server_socket.close()
