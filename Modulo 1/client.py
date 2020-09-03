
#ESTO NO PESCARLO HASTA DESPUES
#para probar el servidor orientado a conexión pueden usar netcat
#nc localhost 8888

import socket

print("Creando socket - Cliente")

#Armamos el socket, el segundo parametro nos dice el tipo de conexion
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Se conecta al puerto
client_socket.connect(('localhost', 8888))

#Mandamos un mensaje
print("... Vamos a mandar cosas")

#Socket debe recibir bytes, asique hay que encodearlo
send_message = 'Hola :S'.encode()

#Enviamos el mensaje por el socket
client_socket.send(send_message)
print("... Mensaje enviado")

#Esperamos una respuesta
message = client_socket.recv(1024)
print("-> Respuesta del servidor: " + message.decode())

#Cerramos conexion
client_socket.close()
