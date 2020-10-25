# Hay que implementar un TCP a partir de un UDP
#   TCP -> Orientado a conexion
#   UDP -> No orientado a conexion
# Hay que hacer las funciones de tcp usando udp
#   -> Las de transmitir, recibir datos y close y accept y eso

# Headers TCP -> Algo que tienen que intercambiarse para cachar que las cosas lleguen bien, ACK

import socket

print('Creando Socket - Servidor')
#Creamos el socket UDP
dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Bindeando socket a puerto 5000')
#Bindeamos el socket udp al puerto
dgram_socket.bind(('localhost', 5000))

while True:
    print('Esperando un mensaje en el servidor')
    msg, address = dgram_socket.recvfrom(1024)

    print('Mensaje recibido: "' + msg.decode() + '", con direccion: ' + str(address))
    if (len(msg) > 0):
        ret = dgram_socket.sendto(msg, address)
        print('Mensaje enviado de vuelta: ' + msg.decode())
