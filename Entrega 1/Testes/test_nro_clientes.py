#!/usr/bin/python3

# O objetivo desse teste a verificaar a quantidade de salas que o servidor consegue criar/administrar sem cair
#	iremos estabelecer 2 conexões tcp com o servidor e aguardar por um valor respondido porta
#	caso o servidor não retorne um número ou não consigamos estabelecer uma conexão houve uma falha

import socket
import time

host    = socket.gethostname()
myip    = socket.gethostbyname(host)
s_port  = 16161
s_ip    = '192.168.0.12'
nro_cli = 0

while True :
	
	try:
		s1 = socket.socket() # Socket para estabelecer conexão com servidor
		s2 = socket.socket()	
		print("	sockets criados [",nro_cli,"]")

		s1.connect((s_ip, s_port))
		s1.send(myip.encode())

		s2.connect((s_ip, s_port))
		s2.send(myip.encode())

		print("	ips enviados [",nro_cli,"]")

		data = s1.recv(1024)
		port = int(data.decode())
		print("	porta 1 recebida [",nro_cli,"]"," [",port,"]")
		data = s2.recv(1024)
		port = int(data.decode())
		print("	porta 2 recebida [",nro_cli,"]"," [",port,"]")

		s1.close()
		s2.close()
		print("	conexões estabelecidas [",nro_cli,"]")

		nro_cli += 1
	except Exception as e:
		print(e)
		break

print(nro_cli," clientes conseguiram uma sala (estabelecer conexão com servidor)")
