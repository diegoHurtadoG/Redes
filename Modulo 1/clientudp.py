import socket

#Creamos el socket como udp
cdgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Creamos el mensaje
send_message = 'Mensaje del UDP'.encode()

print('Enviando mensaje: ' + send_message.decode())
#Enviamos el mensaje
cdgram_socket.sendto(send_message, ('localhost', 5000))

#Esperamos la respuesta echo
msg, address = cdgram_socket.recvfrom(1024)

#Imprimimos la respuesta echo
print('Reibido el mensaje: ' + msg.decode())

#Cerramos el socket
cdgram_socket.close()