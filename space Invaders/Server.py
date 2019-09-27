#!/usr/bin/python3

import threading
import socket
import random
import queue
import time
import os

cli1         = ""
cli2         = ""
port         = 16161
host         = socket.gethostname()
clients      = ["172.16.0.5"] 
mesg_port    = 12346
port_to_play = 16661
state        = {'asteroide' : 1,'nave1': 600,'nave2': 600,'p1' : 'F','p2' : 'F'}
meg_queue    = queue.Queue()

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

	while True:
		state['asteroide'] = random.randint(1,1200)
		data = str(state['asteroide']) + ";" + str(state['nave1']) + ";" + str(state['nave2']) + ";" + str(state['p1']) + ";" + str(state['p2'])
		print("I've sent : ",data," To : ",(cli1,port_to_play))
		sent = sock.sendto(data.encode(),(cli1,port_to_play))
#		sent = sock.sendto(data.encode(),(cli2,port_to_play))
		time.sleep(.5)

	sock.close()

# Duas opções cada sala ter uma porta, ou cada sala ter um identificador que o cliente envia
# Pensar na condição de termino
def receive_client_messages():
	global host
	global mesg_port

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Socket para receber dados do jogo
	print("Bind in ",(host,mesg_port))
	sock.bind((host,mesg_port))

	while True:
		data, addr = sock.recvfrom(4096)
		print("I've received : ",data.decode()," ",addr)


def recieve_clients():
	global port
	global host
	global clients
	global mesg_port

	sessao = False

	s = socket.socket()
	print("Bind in ",(host,port))
	s.bind((host, port))
	s.listen(5)

	while True:
	# Estabelece conexão com cliente
		c1, addr = s.accept()
		data     = c1.recv(1024)
		clients.append(data.decode())
		print("Received : ",data.decode())
	# Estabelece conexão com segundo cliente
#		c2, addr = s.accept()
#		data     = c2.recv(1024)
#		clients.append(data.decode())

		mesg_port += 1
		c1.send(str(mesg_port).encode())
		print("Sent     : ",mesg_port)
#		c2.send(str(port).encode))

		# Lidar com falhas, se vai reestabelcer conexão, etc.
#		try:
#			newpid = os.fork()
#			if newpid == 0:
			# child
		play_game()
		s_mesgs = threading.Thread(target=send_message_client)
		r_mesgs = threading.Thread(target=receive_client_messages)
		s_mesgs.start()
		r_mesgs.start()
#		except:
#			print("Blue Screen")
		# Fechar em outro momento casos mais parametros prescisem ser trocados
		#   Talvez tentar sincronismo
		c1.close()
#		c2.close()

# Main -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

recieve_clients()
