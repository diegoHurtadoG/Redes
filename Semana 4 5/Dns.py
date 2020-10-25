import binascii
import socket

def send_dns_message(address, port):
    #Encabezado con ID 0 (00 00 en hexadecimal), preguntamos por example.com
    #   00 00 -> ID
    #   00 00 -> QR|Opcode|AA|TC|RD|RA|Z|RCODE
    #   00 01 -> QDCOUNT
    #   00 00 -> ANCOUNT
    #   00 00 -> NSCOUNT
    #   00 00 -> ARCOUNT
    header = '00 00 00 00 00 01 00 00 00 00 00 00'.replace(' ','')

    #Data se compone del nombre codificado:
    #   El primer 7 es la longitud de "example"
    #   Despues de las 7 letras, viene un 3 que es la longitud de "com" (el punto separa)
    #   El texto termina con un 00 (despues del 6D)
    #   Despues el 00 01 es el QTYPE, y el sgte 00 01 es el QCLASS
    data = '07 65 78 61 6D 70 6C 65 03 63 6F 6D 00 00 01 00 01'.replace(' ','')

    message = header + data
    server_address = (address, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #Cambiamos el mensaje al formato apropiado (bits) con la libreria
        binascii_msg = binascii.unhexlify(message)
        #Y enviamos
        sock.sendto(binascii_msg, server_address)

        #Y aqui quedara la respuesta a nuestra consulta
        data,_ = sock.recvfrom(4096)
    finally:
        sock.close()
    #Los datos de la respuesta van en hexadecimal, no binario
    return binascii.hexlify(data).decode("utf-8")

print(send_dns_message('8.8.8.8', 53))

# Lo que responde esto puede variar ciertas partes, pero es esto (los '-' los puse yo)
# 000080800001000100000000 - 076578616d706c6503636f6d0000010001 - c00c000100010000526c00045db8d822
#         HEADER                  RESPONSE DATA - QUESTION             RESPONSE DATA - ANSWER

# El 80 80 que hay corresponde al binario 10000000 10000000 que es esa fila con muchos datos que hay en los header
# El RD QUESTION es igual al que se envia
# El RD ANSWER:
#   c00c es el nombre (1100 0000 1100 0000 en binario), los 14 ultimos bits son el offset que indica cuanto
#       hay que contar desde el inicio del mensaje para encontrar el nombre en QNAME
#   Lo otro es relleno standard (se explica en eol), importa la parte final
#   ElRDDATA que recibimos es 5d b8 d8 22 -> 93.184.216.34 direccion ip.

# Con dig -p53 @8.8.8.8 "example.com" recibo la respuesta mas ordenada

