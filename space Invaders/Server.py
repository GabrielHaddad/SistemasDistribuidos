#!/usr/bin/python3

import threading
import socket
import random
import queue
import time
import os

cli1         = "" # ip do cliente 1
cli2         = "" # ip do cliente 2
port         = 16161
host         = socket.gethostname()
clients      = ["172.16.0.5"] 
mesg_port    = 12346
port_to_play = 16661
state        = {'asteroide' : 1,'nave1': 600.0,'nave2': 600.0,'p1' : 'F','p2' : 'F'}
mesg_queue   = queue.Queue()


# Main thread filho
#	Provavelment cli1 e cli2 devem ser locais e passadas para as outras threads
def play_game():
	global clients
	global state
	global cli1
	global cli2

	cli1 = clients.pop()
	cli2 = clients.pop()

#	print(cli1," x ",cli2)
	att_state()

# Thread : atualiza servidor de acordo com mensagens recebidas
def att_state():
	global cli1
	global cli2
	global state
	global mesg_queue

	while True:
		try :
			newstate = mesg_queue.get(timeout=.5)

#			print("I'm alive")
			ip   = newstate[1]
			data = newstate[0].split(";")
			if ip == cli1:
				state['nave1'] = float(data[0])
				state['p1']    = data[1]
			else:
				state['nave2'] = float(dat[0])
				state['p2']    = data[1]
			
#			print("p1 :",state['p1']," p2 :",state['p2'])

			mesg_queue.task_done()
		except  Exception as e:
			print(e)
			pass
		if state['p2'] == 'T' or state['p1'] == 'T' :
#			print("1 - I Died")
			break

# Thread : envio de mensagens para os clientes. Constroi a mensagem e envia para cada um dos n clientes
#  remover state do escopo local
#  remover a parte que da pop dos cliente
def send_message_client():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#	print(cli1," x ",cli2," (",port_to_play,")")

	while True:
		state['asteroide'] = random.randint(1,1200)
		data1 = str(state['asteroide']) + ";" + str(state['nave1']) + ";" + str(state['nave2']) + ";" + str(state['p1']) + ";" + str(state['p2'])
		data2 = str(state['asteroide']) + ";" + str(state['nave2']) + ";" + str(state['nave1']) + ";" + str(state['p2']) + ";" + str(state['p1'])

#		print("I've sent : ",data1," To : ",(cli1,port_to_play))
		sent = sock.sendto(data1.encode(),(cli1,port_to_play))
#		sent = sock.sendto(data2.encode(),(cli2,port_to_play))
		time.sleep(.5)

		if state['p2'] == 'T' or state['p1'] == 'T' :
#			print("2 - I Died")
			sent = sock.sendto(data1.encode(),(cli1,port_to_play))
			sent = sock.sendto(data1.encode(),(cli1,port_to_play))
			sent = sock.sendto(data1.encode(),(cli1,port_to_play))
			break

	sock.close()

# Thread : recebe mensagens do cliente e as coloca em uma fila bloqueante
#	Obs .: clientes são identificados por ip somente (depois mudar para ip e porta)
def receive_client_messages():
	global host
	global mesg_port
	global mesg_queue

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Socket para receber dados do jogo
#	print("Bind in ",(host,mesg_port))
	sock.bind((host,mesg_port))

	while True:
		data, addr = sock.recvfrom(4096)
		mesg_queue.put((data.decode(),addr[0]))
#		print("I've received : ",data.decode()," ",addr[0])

		if state['p2'] == 'T' or state['p1'] == 'T' :
#			print("3 - I Died")
			break

	sock.close()

# Main program (father) : recebe conexões e cria salas (processos filhos)
#	Falta matar filhos e threads com condições de parada
def recieve_clients():
	global cli1
	global cli2
	global port
	global host
	global clients
	global mesg_port

	sessao = False

	s = socket.socket()
#	print("Bind in ",(host,port))
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
#		c2.send(str(port).encode))
		print("Sent     : ",mesg_port)

		c1.close()
#		c2.close()

	# Lidar com falhas, se vai reestabelcer conexão, etc.
		try:
			newpid = os.fork()
			if newpid == 0:
			# child
				print("Child")
				cli1 = clients.pop()
				cli2 = clients.pop()

				print(cli1," x ",cli2)
				s_mesgs = threading.Thread(target=send_message_client)
				r_mesgs = threading.Thread(target=receive_client_messages)
				s_mesgs.start()
				r_mesgs.start()

				att_state()

				s_mesgs.join()
				r_mesgs.join()

				print("I'm dead")
				break
		except:
			print("Blue Screen")
		# Fechar em outro momento casos mais parametros prescisem ser trocados
		#   Talvez tentar sincronismo

# Main -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

recieve_clients()
