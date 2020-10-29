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
import json
import random

#Creamos el socket como udp
import sys

def stopAndWait(sock, msg, address):
    while True:
        try:
            #addHeader(msg, "Contenido", 0000) #todo
            sock.sendto(msg, address)
            retmsg, retaddress = sock.recvfrom(64) #Cambiar esto para que sean mensajes mas grande
            return retmsg, retaddress
        except socket.timeout as e:
            #Aqui deberia hacerle algun cambio al mensaje para que sepa que no es primera vez que mando
            #Sin loss, funciona, con loss se cae (el error esta aqui)
            continue


#Dados un mensaje tipo y numero retorna un json con el formato que estamos usando
def addHeader(msg,tipo,nro):
    #Aqui se puede armar algo tipo json, o algo tipo html
    #Que al mensaje le ponga una estructura consistente
    #Que contenga si es mensaje SYN o mensaje ACK
    #Y que contenga un numero para ir comunicandose, este numero es el de seguimiento y es nro de intervalo de bits
    msg_set = {"Tipo": tipo, "Numero": nro, "Mensaje": msg}
    msg_json = json.dumps(msg_set)
    return msg_json

#Funciona bien
#Dado un socket y un address, conecta al emisor con los parametros.
def handshake(socket, address):
    print("Iniciando Handshake ...")
    numero_ack = random.randint(0, 1000000)
    msg_json = addHeader("", "ACK", numero_ack)

    print("Enviando primer mensaje de handshake: ", msg_json)

    respuesta, dirret = stopAndWait(socket, msg_json.encode(), address)

    print("Recibida respuesta de handshake: ", respuesta.decode())

    json_respuesta = json.loads(respuesta.decode())
    if((json_respuesta["Tipo"] == "ACK + SYN") and (json_respuesta["Numero"] == numero_ack + 1)):
        #Si entre a este if me falta mandar el syn de vuelta
        msg_syn = addHeader(json_respuesta["Mensaje"] + 1, "SYN", None)
        print("Enviando mensaje SYN del handshake: ", msg_syn)
        final, dirRet = stopAndWait(socket, msg_syn.encode(), address)
    else:
        final = "No se completo handshake"

    return final



cdgram_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cdgram_socket.settimeout(0.01)

#Aqui hago el handshako
aprobacion_json = handshake(cdgram_socket, ('localhost', 5000))
aprobacion_json_decoded = aprobacion_json.decode()
aprobacion = json.loads(aprobacion_json_decoded)
if(aprobacion["Mensaje"] != "OK"):
    print("Handshake no se aprobo")
    raise Exception("No se aprobo la conexion")

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
