import socket

#Creamos el socket como udp
import sys

cdgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#De esta forma de abajo, se deberia llamar por consola de la forma
# cat prueba | python3 clientudpfile.py
data = sys.stdin.readlines()

for line in data:
    #Creamos el mensaje
    send_message = line.encode()

    print('Enviando mensaje: ' + send_message.decode())
    #Enviamos el mensaje
    cdgram_socket.sendto(send_message, ('localhost', 5000))

    #Esperamos la respuesta echo
    msg, address = cdgram_socket.recvfrom(1024)

    #Imprimimos la respuesta echo
    print('Reibido el mensaje: ' + msg.decode())

#Cerramos el socket
cdgram_socket.close()