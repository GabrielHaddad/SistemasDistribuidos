#!/usr/bin/python3

import time
import queue
import pygame
import socket
import random
import threading
from pygame.locals import *
from random import randrange

host = socket.gethostname()
myip = socket.gethostbyname(host)
port = 16161          # porta para conectar ao servidor/ seu valor vai provavelmente mudar durante a execução do programa
port_to_play = 16661
s_ip = '192.168.0.12' # ip do servidor

### essa parte nao recebe nem envia mensagens 
synchronized_queue    = queue.Queue(100)
colidiu_2             = False
colidiu_1             = False
vel_dificul           = 1
explodir_nave	      = False 
collided	      = False 
collided_2            = False
pontos		      = 0 #VARIAVEL PONTUACAO
pontuacaototal	      = 0 #VARIAVEL DE CONTROLE DE NIVEIS
tick_musica	      = 0 #VARIAVEL CONTROLADORA DE MUSICA
spawn_de_asteroides   = 800 #SPAWN DE ASTEROIDES DE ACORDO COM PONTUAÇÃO TOTAL
asteroides	      = [] #LISTA DE ASTEROIDES
background_filename   = 'galaxy2.png' 
#asteroidesNewPosition = 0


# SD --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Conecta ao servidor
#	cliente envia o seu ip (provavelment não prescisa)
#	cliente recebe a porta que ele deve enviar as mensagens para o servidor (posição da nave)
def connect_to_server():
	global port

	s = socket.socket() # Socket para estabelecer conexão com servidor

	s.connect((s_ip, port))
	s.send(myip.encode())
	data = s.recv(1024)
	port = int(data.decode())
	s.close()

# Thread que recebe mensagens do servidor 
#	coloca as mensagens em uma fila bloqueantes
# 	Uso de protocolo UDP
#	para quando receber do servidor mensagem que alguem colidiu
def receive_messages():
	global host
	global g_list
	global collided
	global collided_2
	global port_to_play

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Socket para receber dados do jogo
	print("Bind in ",(host,port_to_play))
	sock.bind((host,port_to_play))

	while True:
		data, addr = sock.recvfrom(4096)
		d_list = data.decode().split(";")

		synchronized_queue.put({
			'asteroide' : int(d_list[0]),
			'nave1'     : float(d_list[1]),
			'nave2'     : float(d_list[2]),
			'colidiu_p1': d_list[3],
			'colidiu_p2': d_list[4],
		})

		
		print("I received : ",data.decode())
		if d_list[3] == 'T' or d_list[4] == 'T':
			break

	print("1 - Im dead")
	sock.close()

# Thread de envio de mensagens
#	Função deve ser chamada a cada milesimo de segundo
#	Pega a posicao da nave e a envia em conjunto com collided (que indica se a nave colidiu ou não)
def send_message():
	global collided
	global collided_2

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	while True:
		data = str(nave['posicao'][0])
		
		if collided :
			print("True - T")
			data = data + ";T"
		else :
			print("False - F")
			data = data + ";F"
 
		print("I sent : ",data)
		sent = sock.sendto(data.encode(),(s_ip,port))

		if collided or collided_2:
			print("2 - I'm dead")
			sent = sock.sendto(data.encode(),(host,port))
			print("I sent : ",data)
			sent = sock.sendto(data.encode(),(host,port))
			print("I sent : ",data)
			sent = sock.sendto(data.encode(),(host,port))
			print("I sent : ",data)
			sock.close()
			break

		time.sleep(.1)


# Thread responsavel por atualizar variaveis
#	Le fila bloqueante
#	Cria meteoro se necessário
#	Atualiza posição da nave e variavel collided_2
def atualiza_variaveis():
	global nave2
	global asteroides
	global collided
	global collided_2

	print("Time to att")
	while True :
		try:
			newstate = synchronized_queue.get(timeout=.5)  ## retira  a mensagem da fila

			# Cria asteroide
			if newstate['asteroide'] > 0:
				asteroidesNewPosition = newstate['asteroide']
				asteroides.append(create_asteroide(vel_dificul,asteroidesNewPosition))

			# 'Move' nave 2
			nave2['posicao'][0] = newstate['nave2']
			if newstate['colidiu_p2'] == 'T': ## Servidor vai mandar mensagem para os clientes de modo que o cliente sempre sera a nave1
				collided_2 = True
			print("Nave 2 : ", nave2['posicao'][0]," [",collided_2,"]")

			synchronized_queue.task_done()
		except Exception as e:
			print("Exception : ",e)
			pass

		if collided or collided_2:
			break

	print("3 - I'm dead")

## o loop vai ser feito na funçao que chamar atualiza_variaveis
## Ela é uma thread que atualiza parametros assim que eles estiverem na fila de mensagens
# Game ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def render_scene():
	global screen
	global score_font
	global asteroides
	global pontuacaototal
	global dificuldade_font

	screen.blit(background, (0, 0)) 
	textopontos = score_font.render('PONTUAÇÃO:'+str(pontos)+' ',1 ,(250,250,250))

	for asteroide in asteroides: #BLIT DOS ASTEROIDES NA TELA
		screen.blit(asteroide['tela'], asteroide['posicao'])

	if collided == False and collided_2 == False :
		screen.blit(textopontos, (0,0)) #TXT DO SCORE
	else:
		screen.blit(textopontos, (450, 300)) #TXT DO SCORE QUANDO ACABA O JOGO


	if (pontuacaototal<=9999): #CORES DOS LETREIROS DE DIFICULDADE
		dif1 = dificuldade_font.render('Dificuldade: Iniciante', 1, (255, 255, 255))
		screen.blit(dif1, (0, 22))
	elif (pontuacaototal<=20000):
		dif1 = dificuldade_font.render('Dificuldade: Amador', 1, (30,144,255))
		screen.blit(dif1, (0, 22))
	elif (pontuacaototal<=30000):
		dif1 = dificuldade_font.render('Dificuldade: Intermediário ', 1, (255,255,0))
		screen.blit(dif1, (0, 22))
	elif (pontuacaototal<=40000):
		dif1 = dificuldade_font.render('Dificuldade: Profissional', 1, (255,0,255))
		screen.blit(dif1, (0, 22))
	elif (pontuacaototal<=60000):
		dif1 = dificuldade_font.render('Dificuldade: Star Wars', 1, (255,0,0))
		screen.blit(dif1, (0, 22))

	
	screen.blit(nave['tela'], nave['posicao'])
	screen.blit(nave2['tela'],nave2['posicao'])

def raise_difficulty():
	global vel_dificul
	global pontuacaototal

	if(pontuacaototal >= 1000):
		vel_dificul = 1
	if (pontuacaototal >= 10000):
		vel_dificul = 2
	if (pontuacaototal >= 20000):
		vel_dificul = 3
	if (pontuacaototal >= 30000):
		vel_dificul = 4
	if (pontuacaototal >= 40000):
		vel_dificul = 5
	if (pontuacaototal >= 60000):
		vel_dificul = 6

def get_rect(obj): 
	return Rect(obj['posicao'][0],obj['posicao'][1],obj['tela'].get_width(),obj['tela'].get_height())

def nave_collided():
	nave_rect = get_rect(nave)
	for asteroide in asteroides:
		if nave_rect.colliderect(get_rect(asteroide)):
			return True

	return False

def block_ship():
	global nave

	#POSIÇÃO PARA BARRAR A NAVE
	if(nave['posicao'][0] > 1150):
		nave['posicao'][0] = 1150
	if(nave['posicao'][0] < 0):
		nave['posicao'][0] = 0

def mov_ship():
	global nave

	if pygame.key.get_pressed()[K_a] : 
#		nave['posicao'][0] += -1.5
		nave['posicao'][0] += -7
	
	elif pygame.key.get_pressed()[K_d] :
#		nave['posicao'][0] +=  1.5
		nave['posicao'][0] +=  7

	block_ship()

def create_asteroide(vel_dificul,asteroidesNewPosition):
#	global asteroidesNewPosition

	return {
		'tela'      : pygame.image.load('asteroide1.png').convert_alpha(),
		'posicao'   : [asteroidesNewPosition, -64],                      # Coloca a posição passada pelo servidor
		'velocidade': vel_dificul
	}

def mover_asteroides():
	for asteroide in asteroides:
		asteroide['posicao'][1] += 8

# Main -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

connect_to_server()
      
pygame.init() 
pygame.font.init()

explosion_sound  = pygame.mixer.Sound('boom.wav')
musica_fundo	 = pygame.mixer.Sound('boom.wav')

pygame.display.set_caption('Space Invaders') 

font_name	 = pygame.font.get_default_font()
game_font	 = pygame.font.SysFont(font_name, 72) 
score_font	 = pygame.font.SysFont(font_name, 35) 
level_font	 = pygame.font.SysFont(font_name, 40)
dificuldade_font = pygame.font.SysFont(font_name, 30)
screen           = pygame.display.set_mode((1200, 700)) 
background       = pygame.image.load(background_filename).convert()

nave  = {
	'tela': pygame.image.load('nave.png').convert_alpha(),
	'posicao': [1200/2, 700 - 60], 
	'velocidade': {
		'x': 0,
	}
}

nave2 =  {
	'tela': pygame.image.load('nave.png').convert_alpha(),
	'posicao': [1200/2, 700 - 60], 
	'velocidade': {
		'x': 0,
	}
}

while True:
	try:
		r_mesg = threading.Thread(target=receive_messages)
		s_mesg = threading.Thread(target=send_message)
		att    = threading.Thread(target=atualiza_variaveis)
		r_mesg.start()
		s_mesg.start()
		att.start()
		break
	except:
		print("Error")
		pass
while True:
	ini = time.process_time()	

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	render_scene()
	raise_difficulty()
	mover_asteroides()
	mov_ship()

# quem decide se colidiu é o servidor 
#    cada cliente verifica se colidiu ou não e manda para o servidor

	collided = nave_collided()
	if collided or collided_2:
		print("Collided : ",collided)
		r_mesg.join()
		s_mesg.join()
		att.join()
		break
			
	pontuacaototal += 1 #PONTUAÇÃO SENDO ADICIONADA DENTRO DE UMA VARIAVEL, ANINHADA COM WHILE
	pontos         += 1

	pygame.display.update()

	end = time.process_time()
	idle = 0.0167 - (end - ini)
	time.sleep(idle)

while True :
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	render_scene()

	if not explodir_nave: #CONDIÇÃO DO SISTEMA SONORO CASO A NAVE EXPLODA
		musica_fundo.stop()
		explodir_nave = True 
		explosion_sound.play() 
		nave['posicao'][0] += nave['velocidade']['x']
		
		screen.blit(nave['tela'], nave['posicao'])
	else:
		if collided :
			text = game_font.render('VOCE PERDEU!!', 1, (255, 0, 0)) 			
			screen.blit(text, (450, 350)) #TXT DO GAME OVER APOS O JOGO
		else :	
			text = game_font.render('VOCE GANHOU!!', 1, (0, 255, 0)) 			
			screen.blit(text, (450, 350)) #TXT DO GAME OVER APOS O JOGO

	pygame.display.update()
