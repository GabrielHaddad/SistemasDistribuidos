import pygame
from pygame.locals import *
from random import randrange

pygame.init() 
pygame.font.init()

#VARIAVEIS SONOROS
explosion_sound = pygame.mixer.Sound('boom.wav')
musica_fundo = pygame.mixer.Sound('boom.wav')
explodir_nave = False #CONTROLE SOM GAME OVER
pygame.display.set_caption('Space Invaders') 

#VARIAVEIS GERAIS
collided = False
pontos = 0 #VARIAVEL PONTUACAO
pontuacaototal = 0 #VARIAVEL DE CONTROLE DE NIVEIS
tick_musica = 0 #VARIAVEL CONTROLADORA DE MUSICA
spawn_de_asteroides = 800 #SPAWN DE ASTEROIDES DE ACORDO COM PONTUAÇÃO TOTAL
asteroides = [] #LISTA DE ASTEROIDES
font_name = pygame.font.get_default_font()

#tamanho da fonte(GAME OVER,SCORE,LEVEL)
game_font = pygame.font.SysFont(font_name, 72) 
score_font = pygame.font.SysFont(font_name, 35) 
level_font = pygame.font.SysFont(font_name, 40)
dificuldade_font = pygame.font.SysFont(font_name, 30)

#Tamanho da tela
screen = pygame.display.set_mode((1200, 700)) 

#imagem de fundo
background_filename = 'galaxy2.png' 
background = pygame.image.load(background_filename).convert()



#CRIAR ASTEROIDE
def create_asteroide():
    return {
        'tela': pygame.image.load('asteroide1.png').convert_alpha(),
        'posicao': [randrange(1200), -64],#POSIÇÃO DE ONDE COMEÇA O ASTEROIDE
        'velocidade': randrange(1)
    }

#Nave(imagem da nave, posição e velocidade)
nave = {
    'tela': pygame.image.load('nave.png').convert_alpha(),
    'posicao': [1200/2, 700 - 60], 
    'velocidade': {
        'x': 0,
    }
}

#Segunda Nave(imagem da nave, posição e velocidade)
nave2 = {
    'tela': pygame.image.load('nave2.png').convert_alpha(),
    'posicao': [1200/2, 700 - 60], 
    'velocidade': {
        'x': 0,
    }
}


# PEGA POSIÇÃO DA NAVE 'RECT' E 'RECT' DO ASTEROIDE
def nave_collided():
    nave_rect = get_rect(nave)
    nave_rect2 = get_rect(nave2)
    for asteroide in asteroides:
        if nave_rect.colliderect(get_rect(asteroide)) or nave_rect2.colliderect(get_rect(asteroide)):
            return True

    return False

#MOVIMENTO DOS ASTEROIDES
def mover_asteroides():
    for asteroide in asteroides:
        asteroide['posicao'][1] += asteroide['velocidade']

#OBTER POSIÇÃO DOS OBJETOS
def get_rect(obj): 
    return Rect(obj['posicao'][0],
                obj['posicao'][1],
                obj['tela'].get_width(),
                obj['tela'].get_height())




while True: #CONTROLE DE asteroideS SPAWNADOS POR PONTUAÇÃO
    if not spawn_de_asteroides:
        spawn_de_asteroides = 220
        asteroides.append(create_asteroide())

    else:
        spawn_de_asteroides -= 1

    nave['velocidade'] = {
        'x': 0,
    }

    nave2['velocidade'] = {
        'x': 0,
    }


    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
            
    pontuacaototal += 1 #PONTUAÇÃO SENDO ADICIONADA DENTRO DE UMA VARIAVEL, ANINHADA COM WHILE
    
    #VELOCIDADE DE SE MEXER COM AS SETAS
    if pygame.key.get_pressed()[K_a] : 
     nave['velocidade']['x'] = -1
    elif pygame.key.get_pressed()[K_d] :
     nave['velocidade']['x'] = 1

     #VELOCIDADE DE SE MEXER COM AS SETAS
    if pygame.key.get_pressed()[K_LEFT] : 
     nave2['velocidade']['x'] = -1
    elif pygame.key.get_pressed()[K_RIGHT] :
     nave2['velocidade']['x'] = 1
     
    #DE ONDE COMEÇA O BACKGROUND
    screen.blit(background, (0, 0)) 
    
    #PONTUAÇÃO LETREIRO
    textopontos = score_font.render('PONTUAÇÃO:'+str(pontos)+' ',1 ,(250,250,250))
    #VELOCIDADE DOS asteroideS DE ACORDO COM A PONTUAÇÃO
    if(pontuacaototal >= 1000):
        asteroide['velocidade'] = 1
    if (pontuacaototal >= 10000):
        asteroide['velocidade'] = 1.5
    if (pontuacaototal >= 20000):
        asteroide['velocidade'] = 2
    if (pontuacaototal >= 30000):
        asteroide['velocidade'] = 2.5
    if (pontuacaototal >= 40000):
        asteroide['velocidade'] = 3
    if (pontuacaototal >= 60000):
        asteroide['velocidade'] = 3.5
        
        
    if collided == False:
        screen.blit(textopontos, (0,0)) #TXT DO SCORE
    else:
       screen.blit(textopontos, (450, 300)) #TXT DO SCORE QUANDO ACABA O JOGO
    mover_asteroides()

    for asteroide in asteroides: #BLIT DOS ASTEROIDES NA TELA
        screen.blit(asteroide['tela'], asteroide['posicao'])

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
        
    if not collided: #CONDIÇÃO PARA CASO A NAVE COLIDIR COM ASTEROIDE
        if (tick_musica == 0):
            musica_fundo.play()
            tick_musica += 1
        else:
            tick_musica += 1
        collided = nave_collided() 
        nave['posicao'][0] += nave['velocidade']['x'] 
        nave2['posicao'][0] += nave2['velocidade']['x'] 
        pontos += 1
        screen.blit(nave['tela'], nave['posicao'])
        screen.blit(nave2['tela'], nave2['posicao'])
        
    else:
        if not explodir_nave: #CONDIÇÃO DO SISTEMA SONORO CASO A NAVE EXPLODA
            musica_fundo.stop()
            explodir_nave = True 
            explosion_sound.play() 
            nave['posicao'][0] += nave['velocidade']['x']
            nave2['posicao'][0] += nave2['velocidade']['x']  
            
            
            screen.blit(nave['tela'], nave['posicao'])
            screen.blit(nave2['tela'], nave2['posicao'])
        else:
            text = game_font.render('VOCE PERDEU!!', 1, (255, 0, 0)) 
            
            screen.blit(text, (450, 350)) #TXT DO GAME OVER APOS O JOGO
            
    #POSIÇÃO PARA BARRAR A NAVE
    if(nave['posicao'][0] > 1150):
        nave['posicao'][0] = 1150
    if(nave['posicao'][0] < 0):
        nave['posicao'][0] = 0

    if(nave2['posicao'][0] > 1150):
        nave2['posicao'][0] = 1150
    if(nave2['posicao'][0] < 0):
        nave2['posicao'][0] = 0

    pygame.display.update()
