# Hay que implementar un TCP a partir de un UDP
#   TCP -> Orientado a conexion
#   UDP -> No orientado a conexion
# Hay que hacer las funciones de tcp usando udp
#   -> Las de transmitir, recibir datos y close y accept y eso

# Headers TCP -> Algo que tienen que intercambiarse para cachar que las cosas lleguen bien, ACK

import socket
import json
import random

#Dados un mensaje tipo y numero retorna un json con el formato que estamos usando
def addHeader(msg,tipo,nro):
    #Aqui se puede armar algo tipo json, o algo tipo html
    #Que al mensaje le ponga una estructura consistente
    #Que contenga si es mensaje SYN o mensaje ACK
    #Y que contenga un numero para ir comunicandose, este numero es el de seguimiento y es nro de intervalo de bits
    msg_set = {"Tipo": tipo, "Numero": nro, "Mensaje": msg}
    msg_json = json.dumps(msg_set)
    return msg_json

print('Creando Socket - Servidor')
#Creamos el socket UDP
dgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Bindeando socket a puerto 5000')
#Bindeamos el socket udp al puerto
dgram_socket.bind(('localhost', 5000))

## Aqui empieza el handshake (El while True de afuera)
while True:
    print("Partiendo el handshake...")
    msg_hand_json, address = dgram_socket.recvfrom(1024)
    print("Mensaje handshake recibido: ", msg_hand_json.decode())
    msg_hand = json.loads(msg_hand_json.decode())

    if(msg_hand["Tipo"] == "ACK"):
        num_syn = random.randint(0, 100000)
        msg_hand2 = addHeader(num_syn, "ACK + SYN", msg_hand["Numero"] + 1)
        print("Enviando de vuelta el ACK + SYN", msg_hand2)
        temp = dgram_socket.sendto(msg_hand2.encode(), address)
        continue
    elif((msg_hand["Tipo"] == "SYN") and (msg_hand["Mensaje"] == num_syn + 1)):
        final = addHeader("OK", None, None)
        print("Enviando mensaje final del handshake", final)
        temp = dgram_socket.sendto(final.encode(), address)
    else:
        print("No se completo el handshake")
        break

    ## Aqui termino el handshake y si salio bien entra al while de abajo

    while True:
        print('Esperando un mensaje en el servidor')
        msg, address = dgram_socket.recvfrom(1024)

        print('Mensaje recibido: "' + msg.decode() + '", con direccion: ' + str(address))
        if (len(msg) > 0):
            ret = dgram_socket.sendto(msg, address)
            print('Mensaje enviado de vuelta: ' + msg.decode())
