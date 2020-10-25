import socket
from dnslib import DNSRecord

forward_addr = ("8.8.8.8", 53)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
qname = "example.com"
q = DNSRecord.question(qname)
client.sendto(bytes(q.pack()), forward_addr)
data, _= client.recvfrom(4096)

d = DNSRecord.parse(data)

print("header: ", d.header)
h_id = d.header.id # Cambiar por consulta
h_qr = d.header.qr # 1 si mensaje es respuesta
h_opcode = d.header.opcode # 0 en este caso por ser consultas estandar
h_aa = d.header.aa # 0 si servidor no es autoridad
h_tc = d.header.tc # 0 si el mensaje no fue truncado
h_rd = d.header.rd # 0 si no pedimos recursion
h_ra = d.header.ra # 1 si el que responde acepta recursion
h_rcode = d.header.rcode # 0 si no hubo error

print("q: ", d.q)
q_name = d.q.qname # example.com
q_type = d.q.qtype # 1 si preguntamos por ip, 2 si preguntamos NS
q_class = d.q.qclass # 1 si la clase es tipo IN

#Answer
print("a: ", d.a)
a_name = d.a.rname # example.com
a_type = d.a.rtype # 1 si es IP, 2 si es NS
a_class = d.a.rclass # 1 si la clase es tipo IN
a_ttl = d.a.ttl # Tiempo de validez de la respuesta
a_data = d.a.rdata # Muestra los datos que buscamos, en nuestro caso es la ip

print("r: ", d.rr)
print("ar: ", d.ar)
print("auth: ", d.auth)
print("questions: ", d.questions)
