#!/usr/bin/python3

import threading
import socket
import random
import time

port         = 16161
host         = socket.gethostname()
clients      = ["172.16.0.5"] 
port_to_play = 16661

def play_game():
	global clients

	cli1 = clients.pop()
	cli2 = clients.pop()
	print(cli1," x ",cli2)

	data = str(random.randint(1,666))

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sent = sock.sendto(data.encode(),(cli1,port_to_play))

	sock.close()


def recieve_clients():
	global port
	global host
	global clients

	s = socket.socket()
	s.bind((host, port))
	s.listen(5)

	while True:
		c, addr = s.accept()
		data    = c.recv(1024)
		clients.append(data.decode())

		print(clients)
		if (len(clients) >= 2):
			try:
				x = threading.Thread(target=play_game)
				x.start()
			except:
				print("Error unable to create thread")

		c.close()


# Main -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

recieve_clients()
