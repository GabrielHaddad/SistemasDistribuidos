#!/usr/bin/python3

import queue
import pygame
import socket
import random
import threading
from pygame.locals import *
from random import randrange


### essa parte nao recebe nem envia mensagens 
synchronized_queue  = queue.Queue(100)
colidiu_2           = False
colidiu_1           = False
vel_dificul         = 1
explodir_nave	    = False 
collided	    = False
pontos		    = 0 #VARIAVEL PONTUACAO
pontuacaototal	    = 0 #VARIAVEL DE CONTROLE DE NIVEIS
tick_musica	    = 0 #VARIAVEL CONTROLADORA DE MUSICA
spawn_de_asteroides = 800 #SPAWN DE ASTEROIDES DE ACORDO COM PONTUAÇÃO TOTAL
asteroides	    = [] #LISTA DE ASTEROIDES
background_filename = 'galaxy2.png' 
asteroidesNewPosition=0

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

	if collided == False:
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
#		nave['posicao'][0] += -1
		nave['posicao'][0] += -1
	
	elif pygame.key.get_pressed()[K_d] :
#		nave['posicao'][0] +=  1
		nave['posicao'][0] +=  1

	block_ship()

def mover_asteroides():
	for asteroide in asteroides:
		asteroide['posicao'][1] = asteroidesNewPosition

def atualiza_variaveis():
	global nave2
	global asteroidesNewPosition
	try:
		newstate = synchronized_queue.get()  ## retira  a mensagem da fila 
		asteroidesNewPosition = newstate['asteroides']
		nave2['position'][0]=newstate['nave2']
		collided = newstate['colidiu_p1']        ## 1 ou dois como que vou saber se o servidor nao dizer ?
		#collided = newstate['colidiu_p2']
	except:
		pass
## o loop vai ser feito na funçao que chamar atualiza_variaveis
      
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
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

#	if not spawn_de_asteroides:
#		spawn_de_asteroides = 220
#		asteroides.append(create_asteroide(vel_dificul))
#	else:
#		spawn_de_asteroides -= 1

	
	raise_difficulty()
	mover_asteroides()
	mov_ship()

# quem decide se colidiu é o servidor 

	if collided :
		break
			
	pontuacaototal += 1 #PONTUAÇÃO SENDO ADICIONADA DENTRO DE UMA VARIAVEL, ANINHADA COM WHILE
	pontos         += 1
        render_scene()
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
		text = game_font.render('VOCE PERDEU!!', 1, (255, 0, 0)) 			
		screen.blit(text, (450, 350)) #TXT DO GAME OVER APOS O JOGO
	
	render_scene()
	pygame.display.update()
