# Hay que implementar un TCP a partir de un UDP
#   TCP -> Orientado a conexion
#   UDP -> No orientado a conexion
# Hay que hacer las funciones de tcp usando udp
#   -> Las de transmitir, recibir datos y close y accept y eso

# Headers TCP -> Algo que tienen que intercambiarse para cachar que las cosas lleguen bien, ACK
# Header es informacion basica necesaria: Tipo (ACK o SYN)
#                                         Nro Secuencia (Para saber que responder)

#El 3 way handshake es:
# SYN       ->
# SYN + ACK <-
# ACK       ->

import socket
import time

#Creamos el socket como udp
import sys

def stopAndWait(sock, msg, address):
    while True:
        try:
            sock.sendto(msg, address)
            retmsg, retaddress = sock.recvfrom(64) #Cabmiar esto para que sean mensajes mas grande
            return retmsg, retaddress
        except socket.timeout as e:
            #Aqui deberia hacerle algun cambio al mensaje para que sepa que no es primera vez que mando
            #Sin loss, funciona, con loss se cae (el error esta aqui)
            continue

def addHeader(msg):
    #Aqui se puede armar algo tipo json, o algo tipo html
    #Que al mensaje le ponga una estructura consistente
    #Que contenga si es mensaje SYN o mensaje ACK
    #Y que contenga un numero para ir comunicandose, este numero es el de seguimiento y no es random
    pass

cdgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cdgram_socket.settimeout(0.01)

#De esta forma de abajo, se deberia llamar por consola de la forma
# cat prueba | python3 clientudpfile.py
data = sys.stdin.readlines()

for line in data:
    #Creamos el mensaje
    send_message = line.encode()

    print('Enviando mensaje: ' + send_message.decode())

    #Esto de aqui abajo incluye el send y el recv
    msg, address = stopAndWait(cdgram_socket, send_message, ('localhost', 5000))

    # Enviamos el mensaje
    #cdgram_socket.sendto(send_message, ('localhost', 5000))

    # Esperamos la respuesta echo
    #msg, address = cdgram_socket.recvfrom(1024)

    #Imprimimos la respuesta echo
    print('Reibido el mensaje: ' + msg.decode())

#Cerramos el socket
cdgram_socket.close()

def headerTCP(msg):
    pass
