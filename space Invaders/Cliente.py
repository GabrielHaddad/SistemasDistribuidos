#!/usr/bin/python3

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
#s_ip = '192.168.0.12' # ip do servidor

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

	
	screen.blit(nave2['tela'],nave2['posicao'])
	screen.blit(nave['tela'], nave['posicao'])

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
		nave['posicao'][0] += -2
	
	elif pygame.key.get_pressed()[K_d] :
#		nave['posicao'][0] +=  1.5
		nave['posicao'][0] +=  2

	block_ship()

def create_asteroide(vel_dificul,asteroidesNewPosition):
#	global asteroidesNewPosition

	return {
		'tela'      : pygame.image.load('asteroide1.png').convert_alpha(),
		'posicao'   : [randrange(1200), -64],                      # Coloca a posição passada pelo servidor
		'velocidade': vel_dificul
	}

def mover_asteroides():
	for asteroide in asteroides:
		asteroide['posicao'][1] += 1

# SD --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Conecta ao servidor
#	cliente envia o seu ip (provavelment não prescisa)
#	cliente recebe a porta que ele deve enviar as mensagens para o servidor (posição da nave)
def connect_to_server():
	global port

	s = socket.socket() # Socket para estabelecer conexão com servidor

	s.connect((host, port))
	s.send(myip.encode())
	data = s.recv(1024)
	port = int(data.decode())
	s.close()

# thread que recebe mensagens do servidor e coloca elas em uma fila bloqueantes
# 	Uso de protocolo UDP
#	Seems like it'working
#	Obs .: Há a possibilidade da primeira mensagem não estar sendo recebida
def receive_messages():
	global host
	global g_list
	global port_to_play

	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Socket para receber dados do jogo
	print("Bind in ",(host,port_to_play))
	sock.bind((host,port_to_play))

	while True:
		data, addr = sock.recvfrom(4096)
		d_list = data.decode().split(";")

		synchronized_queue.put({
			'asteroide' : int(d_list[0]),
			'nave1'     : int(d_list[1]),
			'nave2'     : int(d_list[2]),
			'colidiu_p1': d_list[3],
			'colidiu_p2': d_list[4],
		})

#		print("I received : ",int(d_list[0])," [",synchronized_queue.qsize(),"]")

	sock.close()

# thread de envio de mensagens
#	Acrescentar campo colidiu na mensagem e o modo do servidor lidar com isso
#	Função deve ser invocada quando o player usa uma tecla para mover ?
#	Função deve ser chamada a cada milesimo de segundo ?
def send_message():
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	data = str(nave['posicao'][0])
#	print("I sent : ",data)
	sent = sock.sendto(data.encode(),(host,port))

def atualiza_variaveis():
	global nave2
	global asteroides
#	global asteroidesNewPosition

	print("Time to att")
	while True :
		try:
			newstate = synchronized_queue.get()  ## retira  a mensagem da fila

			# Cria asteroide 
			asteroidesNewPosition = newstate['asteroide']
			asteroides.append(create_asteroide(vel_dificul,asteroidesNewPosition))

			# 'Move' nave 2
			nave2['position'][0] = newstate['nave2']
#			collided = newstate['colidiu_p1']        ## 1 ou dois como que vou saber se o servidor nao dizer ?
			collided = newstate['colidiu_p2']        ## Servidor vai mandar mensagem para os clientes de modo que o cliente sempre sera a nave1

			synchronized_queue.task_done()
		except:
			pass
## o loop vai ser feito na funçao que chamar atualiza_variaveis
## Ela é uma thread que atualiza parametros assim que eles estiverem na fila de mensagens
      
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

connect_to_server()

while True:
	try:
		r_mesg = threading.Thread(target=receive_messages)
		att    = threading.Thread(target=atualiza_variaveis)
		r_mesg.start()
		att.start()
		break
	except:
		print("Error")
		pass
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

# Quem deve chamar append e create é o atualiza variaveis
#	if not spawn_de_asteroides:
#		spawn_de_asteroides = 220
#		asteroides.append(create_asteroide(vel_dificul,2))
#	else:
#		spawn_de_asteroides -= 1

	render_scene()
	raise_difficulty()
	mover_asteroides()
	mov_ship()

# quem decide se colidiu é o servidor 
#    cada cliente verifica se colidiu ou não e manda para o servidor

	collided = nave_collided()
	if collided or collided_2:
		break
			
	pontuacaototal += 1 #PONTUAÇÃO SENDO ADICIONADA DENTRO DE UMA VARIAVEL, ANINHADA COM WHILE
	pontos         += 1

	pygame.display.update()

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
		if not collided :
			text = game_font.render('VOCE PERDEU!!', 1, (255, 0, 0)) 			
			screen.blit(text, (450, 350)) #TXT DO GAME OVER APOS O JOGO
		else :	
			text = game_font.render('VOCE GANHOU!!', 1, (0, 255, 0)) 			
			screen.blit(text, (450, 350)) #TXT DO GAME OVER APOS O JOGO

	pygame.display.update()
