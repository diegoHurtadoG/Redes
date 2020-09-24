import socket
import json

print("Creando proxy")

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

        #Ver diferencia entre connect y bind, por ahi va el tema del cliente y servidor quiza.
        #Bind dice al SO: "Cuando llegue un mensaje a ese puerto, mandaselo a este proceso"
        #Connect le dice al SO: "Este socket se quiere conectar a esta direccion, mandale un msg"

        #No se tiene que reenviar exactamente lo que se recibe, hay que poner bien los headers y everything

        #received_message tiene el texto que recibimos del cliente y tenemos que enviar al servidor
        #Para esto tenemos que hacer una conexion con el servidor al que queremos enviar y hacer una
        #   mini version de lo que ya hicimos, esperar mensaje de vuelta y ese mandarselo al cliente
# cliente -> received_message en proxy -> envia al servidor -> espera respuesta (server_msg) -> envia al cliente

        #Recibimos -> armamos la consulta (como en el servidor) -> enviamos, recibimos, armamos y mostramos

        connection.send(server_msg.encode())

        #Esperamos el siguiente mensaje
        #Esto de aqui abajo lo hice para que despues de cargar un request, no se quede pegado en el while
        #   porque si no lo hacia, no cargaba la pagina
        buffer = ''


    #Cerramos la conexion
    #Notar que el puerto que se va a imprimir no va a ser el 8888
    connection.close()
    print('Conexion con ' + str(address) + ' ha sido cerrada.')

    #Aqui seguimos esperando por si llegan otras conexiones.