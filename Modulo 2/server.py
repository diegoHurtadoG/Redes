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

    #Recibimos los datos contenidos en el paquete, en trozos de 1024
    #Esto deberia ser bloqueante
    buffer = connection.recv(1024)

    while len(buffer) > 0: #Esto se hace por si por error pasa algun mensaje vacio
        #Decodeamos el mensaje e imprimimos
        received_message = buffer.decode()
        print('-> Mensaje recibido: ' + received_message)

        #Respondemos
        #El mensaje de respuesta es el mismo que recibe pero cambiando la primera linea por el codigo de exito
        #response_message = received_message.encode()
        mensaje = "Mensaje Bienvenida"
        response_message = 'HTTP/1.1 200 OK\r\n'\
                           'Content-Type: text/html; charset=UTF-8\r\n' \
                           'Content-Length: ' + str(len(mensaje)) + '\r\n'\
                           'Autor: X-diegohurtado@ug.uchile.cl\r\n\r\n' \
                           '<html>\r\n' \
                           '    <body>\r\n' \
                           '        <p> ' + 'Hola' + '\r\n' \
                           '    </body>\r\n' \
                           '</html>'

        connection.send(response_message.encode())
        print('LLegue aqui')

        #Esperamos el siguiente mensaje
        #Esto de aqui abajo lo hice para que despues de cargar un request, no se quede pegado en el while
        #   porque si no lo hacia, no cargaba la pagina
        buffer = ''

        # El problema del browser es que se me queda pegado en el while

    #Cerramos la conexion
    #Notar que el puerto que se va a imprimir no va a ser el 8888
    connection.close()
    print('Conexion con ' + str(address) + ' ha sido cerrada.')

    #Aqui seguimos esperando por si llegan otras conexiones.