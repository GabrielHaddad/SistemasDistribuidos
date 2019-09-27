#!/usr/bin/python3

import threading
import socket
import random
import time
import os

cli1         = ""
cli2         = ""
port         = 16161
host         = socket.gethostname()
clients      = ["172.16.0.5"] 
mesg_port    = 12346
port_to_play = 12345
state        = {'asteroide' : 1,'nave1': 600,'nave2': 600,'p1' : 'F','p2' : 'F'}

def play_game():
	global clients
	global state
	global cli1
	global cli2

	cli1 = clients.pop()
	cli2 = clients.pop()

# Uma  threads de envio de mensagens para os clientes. Constroi a mensagem e envia para cada um dos n clientes
#  remover state do escopo local
#  remover a parte que da pop dos cliente
def send_message_client():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	print(cli1," x ",cli2," (",port_to_play,")")
	print("2 : ",state)

	while True:
		state['asteroide'] = random.randint(1,666)
		data = str(state['asteroide']) + ";" + str(state['nave1']) + ";" + str(state['nave2']) + ";" + str(state['p1']) + ";" + str(state['p2'])
		print("1 : ",data)
		sent = sock.sendto(data.encode(),(cli1,port_to_play))

	sock.close()

# Duas opções cada sala ter uma porta, ou cada sala ter um identificador que o cliente envia
# Pensar na condição de termino
def receive_client_messages():
	global host
	global mesg_port

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Socket para receber dados do jogo
	sock.bind((host,mesg_port))

	while True:
		data, addr = sock.recvfrom(4096)
		print(data.decode())


def recieve_clients():
	global port
	global host
	global clients

	sessao = False

	s = socket.socket()
	s.bind((host, port))
	s.listen(5)

	while True:
	# Estabelece conexão com cliente
		c1, addr = s.accept()
		data     = c1.recv(1024)
		clients.append(data.decode())

	# Estabelece conexão com segundo cliente
		c2, addr = s.accept()
		data     = c2.recv(1024)
		clients.append(data.decode())

		port += 1
		c1.send(str(port).encode))
		c2.send(str(port).encode))

		# Lidar com falhas, se vai reestabelcer conexão, etc.
		try:
			newpid = os.fork()
			if newpid == 0:
			# child
				x = threading.Thread(target=play_game)
				x.start()
		except:
			print("Blue Screen")
		# Fechar em outro momento casos mais parametros prescisem ser trocados
		#   Talvez tentar sincronismo
		c1.close()
		c2.close()

# Main -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

recieve_clients()
