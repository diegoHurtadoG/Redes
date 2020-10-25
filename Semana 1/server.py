import socket

print("Creando socket - Servidor")

#Armamos el socket, el segundo parametro es tipo de conexion
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Lo conectamos al servidor, en este caso espera mensajes en el 8888
server_socket.bind(('localhost', 8888))

#Hacemos que sea un server socket y le damos 3 como numnero de posibles
#   peticiones en cola
server_socket.listen(3)

#Esepramos a que llegue alguna peticion de conexion
print('...Esperando Cliente')
while True:
    #Cuando llega una peticion la aceptamos
    #Y luego sacamos los datos de la conexion entrante (objeto, direccion)
    connection, address = server_socket.accept()

    #Recibimos los datos contenidos en el paquete, en trozos de 64
    #Esto deberia ser bloqueante
    buffer = connection.recv(64)

    while len(buffer) > 0: #Esto se hace por si por error pasa algun mensaje vacio
        #Decodeamos el mensaje e imprimimos
        received_message = buffer.decode()
        print('-> Mensaje recibido: ' + received_message)

        #Respondemos
        response_message = ('Mensaje "' + received_message + '" ha sido recibido con exito').encode()
        connection.send(response_message)

        #Esperamos el siguiente mensaje
        #Si no hay mas mensajes, len(buffer) = 0 y salimos del while
        buffer = connection.recv(64)

    #Cerramos la conexion
    #Notar que el puerto que se va a imprimir no va a ser el 8888
    connection.close()
    print('Conexion con ' + str(address) + ' ha sido cerrada.')

    #Aqui seguimos esperando por si llegan otras conexiones.