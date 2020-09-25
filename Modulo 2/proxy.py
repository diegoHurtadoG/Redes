import socket
import json

print("Creando proxy")

#Me ayude de geeks for geeks para la creacion de este codigo

#Armamos el socket, el segundo parametro es tipo de conexion
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Lo conectamos al servidor, en este caso espera mensajes en el 8888
proxy_socket.bind(('localhost', 8888))

#Hacemos que sea un server socket y le damos 3 como numnero de posibles
#   peticiones en cola
proxy_socket.listen(3)

#Esepramos a que llegue alguna peticion de conexion
print('...Esperando Cliente')
while True:
    #Cuando llega una peticion la aceptamos
    #Y luego sacamos los datos de la conexion entrante (objeto, direccion)
    connection, address = proxy_socket.accept()

    #Recibimos los datos contenidos en el paquete, en trozos de 1024
    #Esto deberia ser bloqueante
    buffer = connection.recv(1024)

    while len(buffer) > 0: #Esto se hace por si por error pasa algun mensaje vacio

        #Decodeamos el mensaje e imprimimos
        received_message = buffer.decode()
        print('-> Mensaje recibido: ' + received_message)


        primera_linea = received_message.split('\n')[0]
        url = primera_linea.split(' ')[1] #Aqui tengo http://anakena.dcc.uchile.cl/


        #Teniendo esto hay que llegar hasta el address del destino:
        http_pos = url.find("://") # Posicion del ://
        if(http_pos == -1):
            buf = url
        else:
            buf = url[(http_pos + 3):] # Obtiene el url entero

        # Posicion del puerto de destino
        dest_port_pos = buf.find(":")

        # Encuentra el final del servidor web
        webserver_pos = buf.find("/")
        if webserver_pos == -1:
            webserver_pos = len(buf)

        webserver = ""
        port = -1

        if(dest_port_pos == -1 or webserver_pos < dest_port_pos):
            #Puerto que se usa por default es el 80
            port = 80
            webserver = buf[:webserver_pos]
        else: #Tenemos un puerto especifico
            port = int((buf[(dest_port_pos + 1):])[:webserver_pos-dest_port_pos-1])
            webserver = buf[:dest_port_pos]

        print('Primera linea es: ' + primera_linea) #GET http://anakena.dcc.uchile.cl:8989/ HTTP/1.1
        print('El url es: ' + url) #http://anakena.dcc.uchile.cl:8989/
        print('Posicion del :// ' + str(http_pos)) #4
        print('Webserver es: ' + webserver) #anakena.dcc.uchile.cl
        print('Port es: ' + str(port)) #8989


        #Creamos el socket para el server, segundo parametro cambiable si no funciona
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((webserver, port))

        server_socket.send(received_message.encode())

        while True:
            #Recibimos datos desde el webserver
            data = server_socket.recv(1024)
            if (len(data) > 0):
                connection.send(data) #manda al browser/cliente
            else:
                break

        server_socket.close()


        #Esperamos el siguiente mensaje
        #Esto de aqui abajo lo hice para que despues de cargar un request, no se quede pegado en el while
        #   porque si no lo hacia, no cargaba la pagina
        buffer = ''


    #Cerramos la conexion
    #Notar que el puerto que se va a imprimir no va a ser el 8888
    connection.close()
    print('Conexion con ' + str(address) + ' ha sido cerrada.')

    #Aqui seguimos esperando por si llegan otras conexiones.