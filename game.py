import pygame
import random
import math
import time
from pygame import mixer

pygame.init()
 
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders")

playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
player_change_x = 0

num_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemy_change_x = []
enemy_change_y = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('space-enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemy_change_x.append(0.4)
    enemy_change_y.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_change_x = 0
bullet_change_y = 2
bullet_status = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf',32)
scoreX = 10
scoreY = 10

mixer.music.load('background.wav')
mixer.music.play(-1)

over_font = pygame.font.Font('freesansbold.ttf',64)


def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_status
    bullet_status = 'fire'
    screen.blit(bulletImg,(x+16,y+10))

def collision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score_value = font.render("Score : "+ str(score),True,(255,255,255))
    screen.blit(score_value,(x,y))

def game_over():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(210,250))

running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # print("A key is pressed")
            if event.key == pygame.K_LEFT:
                player_change_x = -0.7
                # print("Left Key is pressed")
            if event.key == pygame.K_RIGHT:
                player_change_x = 0.7
                # print("Right Key is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_status is 'ready':
                    fire_sound = mixer.Sound('laser.wav')
                    fire_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
                # print("Space is pressed")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change_x = 0.0
                # print("Key up")

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
            
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over()
                
        enemyX[i] += enemy_change_x[i]

        if enemyX[i] <= 0:
            enemy_change_x[i] = 0.4
            enemyY[i] += enemy_change_y[i]
        elif enemyX[i] >= 736:
            enemy_change_x[i] = -0.4
            enemyY[i] += enemy_change_y[i]

        collision_check = collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision_check == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_status = 'ready'
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
            score += 1
            print(score)
        
        enemy(enemyX[i],enemyY[i],i)

    if bulletY <= 0:
        bulletY = 480
        bullet_status = 'ready'
        
    if bullet_status is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bullet_change_y
        

    

    playerX += player_change_x
    player(playerX,playerY)
    show_score(scoreX,scoreY)
    pygame.display.update()