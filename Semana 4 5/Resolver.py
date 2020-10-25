#EL RESOLVER NO ES AUTORIDAD DE NINGUNA ZONA, EL MENSAJE SE CAMBIA
#LA RECURSIVIDAD SE HACE HASTA TENER UNA RESPUESTA O HASTA QUE APAREZCA ALGO != NOERROR EN STATUS

# Parsing se puede hacer con libreria

import socket
from dnslib import DNSRecord

def resolver(domain): #DGRAM es no orientado a conexion
    address = ("192.33.4.12", 53) #No se si el primero es eso, localhost, o que. El puerto 5353 no funciona. "192.33.4.12"
    #Si pregunto a "192.33.4.12"
    #Despues a la primera de la additional section -> "190.124.27.10"
    #Despues a la primera de la additional section -> "200.89.70.3"
    #Recibo respuesta (ANSWER: 1) y ahi esta el ip uchile "200.89.76.36"

    #Me hago el socket
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Esto parsea la conslta de una en teoria
    question = DNSRecord.question(domain)
    dns_socket.sendto(bytes(question.pack()), address)

    #Espero respuesta
    data, _ = dns_socket.recvfrom(1024)

    #########################################
    #Aqui empiezo el parsing de la respuesta
    d = DNSRecord.parse(data)
    print("d: ", d)

    print("autoridades: ", d.auth[0]) #Con esto separo una instancia de la seccion autoridad (la primera)

    print("header: ", d.header)
    h_id = d.header.id  # Cambiar por consulta
    h_qr = d.header.qr  # 1 si mensaje es respuesta
    h_opcode = d.header.opcode  # 0 en este caso por ser consultas estandar
    h_aa = d.header.aa  # 0 si servidor no es autoridad
    h_tc = d.header.tc  # 0 si el mensaje no fue truncado
    h_rd = d.header.rd  # 0 si no pedimos recursion
    h_ra = d.header.ra  # 1 si el que responde acepta recursion
    h_rcode = d.header.rcode  # 0 si no hubo error

    print("q: ", d.q)
    q_name = d.q.qname  # example.com
    q_type = d.q.qtype  # 1 si preguntamos por ip, 2 si preguntamos NS
    q_class = d.q.qclass  # 1 si la clase es tipo IN

    # Answer, ESTO SOLO VA A SER NO NULO EN LA ULTIMA ITERACION, antes de eso tira error
    if(d.a is not None):
        print("a: ", d.a)
        a_name = d.a.rname  # example.com
        a_type = d.a.rtype  # 1 si es IP, 2 si es NS
        a_class = d.a.rclass  # 1 si la clase es tipo IN
        a_ttl = d.a.ttl  # Tiempo de validez de la respuesta
        a_data = d.a.rdata  # Muestra los datos que buscamos, en nuestro caso es la ip

    #Aqui ya tengo la respuesta parseada
    #########################################

resolver("www.uchile.cl.")