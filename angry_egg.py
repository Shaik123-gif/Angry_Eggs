import pygame
import random
from pygame import mixer
import math

pygame.init()
screen = pygame.display.set_mode((1020, 480))
pygame.display.set_caption("HALF BOILED EGG")
icon = pygame.image.load('eggs.png')
pygame.display.set_icon(icon)
back = pygame.image.load('background.png')
bask = pygame.image.load('basket.png')




#danger
dangerX = []
dangerY = []
dangerC = []
v = 0
danger_img = []
no_danger = 2
bom = pygame.image.load('bomb.png')
for i in range(no_danger):
    danger_img.append(pygame.image.load('angry-bird-black-icon.png'))
    dangerX.extend([100,500])
    dangerY.append(30)
    dangerC.append(2)


#basket
basketX = 495
basketY = 382
basketC = 0
ch = 1

#bird
birdX = []
birdY = []
birdC = []
bird_img = []
no_birds = 5

#egg
eggX = 300
eggY = 100
eggC = 2
egg_state = "ready"
egg_img = pygame.image.load('egg.png')

#collision
score_value = 0
miss = 3
ch = 0

def iscollision(eX,eY,bX,bY):
    distM = math.sqrt((math.pow(eX - bX,2)) + (math.pow(eY - bY,2)))
    distL = math.sqrt((math.pow((eX-80) - (bX-80), 2)) + (math.pow((eY-80) - (bY-80), 2)))
    distR = math.sqrt((math.pow((eX + 120) - (bX + 120), 2)) + (math.pow((eY + 120) - (bY + 120), 2)))
    if distM < 40 or distL < 60 or distR < 40 :
        mix = mixer.Sound('smb_coin.wav')
        mix.play()
        return True
    else:
        return False

def iscollision_bomb(eX,eY,bX,bY):
    distM = math.sqrt((math.pow(eX - bX,2)) + (math.pow(eY - bY,2)))
    distL = math.sqrt((math.pow((eX - 80) - (bX - 80), 2)) + (math.pow((eY - 80) - (bY - 80), 2)))
    distR = math.sqrt((math.pow((eX + 120) - (bX + 120), 2)) + (math.pow((eY + 120) - (bY + 120), 2)))
    if distM < 40 or distL < 60 or distR < 40:
        return True
    else:
        return False




#bom
bomX = 300
bomY = 10
bomC = 2.5
bom_state = "ready"
bom_img = pygame.image.load('bomb.png')

#score
active = True
font = pygame.font.Font('freesansbold.ttf',32)
over_font = pygame.font.Font('freesansbold.ttf',64)

for i in range(no_birds):
    bird_img.append(pygame.image.load('bird1.png'))
    birdX.extend([-200,0,200,400,600])
    birdY.append(30)
    birdC.append(2)

def basket(x,y):
    screen.blit(bask,(x,y))

def bird(x,y,i):
    screen.blit(bird_img[i],(x,y))

def danger(x,y,i):
    screen.blit(danger_img[i],(x,y))

def bomb(x,y):
   screen.blit(bom,(x,y+10))
   screen.blit(bom,(x+500,y+10))


def egg(x,y):
    screen.blit(egg_img,(x,y+10))

def show_Score(x,y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_Over():
    gameover = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gameover, (300, 150))

def show_Miss(x,y):
        misses = font.render("Lives : " + str(miss), True, (255, 255, 255))
        screen.blit(misses, (x, y))
def play_back(p):
    if p == 0:
        mixer.music.load('backsound.wav')
        mixer.music.play(-1)
    else:
        mixer.music.stop()

play_back(0)

running = True
while running:
    screen.blit(back, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                basketC = 10
            if event.key == pygame.K_LEFT:
                basketC = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                basketC = 0
            if event.key == pygame.K_LEFT:
                basketC = 0
    basketX = basketX + basketC

    if basketX >= 956:
        basketX = 956
    if basketX <= 0:
        basketX = 0

    basket(basketX, basketY)


    for i in range(no_birds):
        birdX[i] = birdX[i] + birdC[i]
        if miss == 0:
            egg_state = "drop"
            active = False
            break
        if birdX[i] >= 956:
            birdX[i] = random.randint(0,956)
        if egg_state == "ready":
            bird_coordinates = birdX[i]
            egg_state = "drop"
        bird(birdX[i],birdY[i],i)
    for i in range(no_danger):
        dangerX[i] = dangerX[i] + dangerC[i]
        if miss == 0:
            active = False
            break
        if dangerX[i] >= 956:
            if v == 1:
                dangerX[i] = random.randint(0, 300)
                if bom_state == "ready":
                    exp = mixer.Sound('explosion.wav')
                    exp.play()
                    danger_coordinates = dangerX[i]
                    bom_state = "drop"
                    v = 0
            elif v == 0:
                dangerX[i] = random.randint(301,956)
                v = 1
        danger(dangerX[i],dangerY[i],i)

    coll = iscollision(eggX,eggY,basketX, basketY)


    if coll:
        eggY = 100
        egg_state = "ready"
        score_value = score_value + 1

    if egg_state == "drop"  and active == True:
        eggX = bird_coordinates
        eggY = eggY + eggC
        egg(eggX,eggY)

    if eggY == 460:
        eggY = 50
        if ch == 0:
            ch = 1
        elif ch == 1:
            miss = miss - 1
            misses = mixer.Sound('miss.wav')
            misses.play()
        egg_state = "ready"
    if bom_state == "drop" and active == True:
        bomX = danger_coordinates
        bomY = bomY + bomC
        bomb(bomX,bomY)
    if bomY == 440:
        bomY = 50
        bom_state = "ready"
    show_Score(0,445)
    show_Miss(850,445)

    coll_bomb1 = iscollision_bomb(bomX, bomY, basketX, basketY)
    coll_bomb2 = iscollision_bomb(bomX+500, bomY, basketX, basketY)

    if coll_bomb1 or coll_bomb2:
            bomY = -2000
            bom_state = "ready"
            active = False
            game_Over()

    if active == False:
        play_back(1)
        miss = 0
        game_Over()
        mis = mixer.Sound('gameover.wav')
        mis.play(-1)

    pygame.display.update()