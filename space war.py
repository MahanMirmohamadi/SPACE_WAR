# import - 120-400
import pygame
import random
import math
from pygame import mixer
pygame.init()
# --------------------------------------------------------------------------
# Main Screen
screen = pygame.display.set_mode((600,957)) 
# ----------------------------------------------------------------------------
# background
wallpaper = pygame.image.load("F:\images\space war/background-wallpaper.jpg")
# ----------------------------------------------------------------------------
# background music
mixer.music.load("F:\other\SPACE WAR GAME/background.mp3")
mixer.music.play(-1)
# ----------------------------------------------------------------------------
# Title and Icon
pygame.display.set_caption("SPACE WAR")
icon = pygame.image.load("F:\images\space war\icon.png")
pygame.display.set_icon(icon)
# --------------------------------------------------------------------------------
# Player 
playerImg = pygame.image.load("F:\images\space war\player.png")
playerX = 268
playerY = 720
playerX_change = 0 
# ---------------------------------------------------------------------------------
# enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = [] 
enemyY_change = [] 
num_of_enemies = 4 
for i in range(num_of_enemies):
    enemyType = random.randint(1,4)
    if enemyType == 1 :
        enemyImg.append(pygame.image.load("F:\images\space war\enemy1.png"))
    elif enemyType == 2 :
        enemyImg.append(pygame.image.load("F:\images\space war\enemy2.png"))
    elif enemyType == 3 :
        enemyImg.append(pygame.image.load( "F:\images\space war\enemy3.png"))
    elif enemyType == 4 :
        enemyImg.append(pygame.image.load("F:\images\space war\enemy4.png"))
    enemyX.append(random.randint(100,400))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(10)
# ----------------------------------------------------------------------------------
# bullet 
bulletImg = pygame.image.load("F:\images\space war/bullet.png")
bulletX = 0
bulletY = 720
bulletX_change = 0.1 
bulletY_change = 1
bullet_state = "ready"
# ----------------------------------------------------------------------------------
# score display
score = 0
font = pygame.font.Font("F:\other\SPACE WAR GAME\Vazirmatn-Black.ttf" , 40)
scorex = 10
scorey = 10
# ----------------------------------------------------------------------------------
# game over display
font1 = pygame.font.Font("F:\other\SPACE WAR GAME\Vazirmatn-Black.ttf" , 60)
gameoverx = 120
gameovery = 400
# ------------------------------------------------------------------------------------
# funcations
def fire_bullet(x,y):
    screen.blit(bulletImg,(x+10,y+20))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i] ,(x,y))

def isCollision(x1,y1,x2,y2):
    distance = math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
    if distance < 30 :
        return True
    else :
        return False
    
def score_display(x , y):
    scoretext = font.render("SCORE: " + str(score) , True , (255 , 255 , 255))
    screen.blit(scoretext , (x , y))

def gameover_display(x , y):
    gameover_text = font1.render("GAME OVER" , True , (255 , 255 , 255))
    screen.blit(gameover_text , (x , y))
# -----------------------------------------------------------------------------------------
# Game Frames 
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    bullet_state = "fire"
                    fire_bullet(bulletX,bulletY)
                    fire_sound = mixer.Sound("F:\other\SPACE WAR GAME\laser.wav")
                    fire_sound.play()

        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerX_change = 0


    screen.fill((0,128,128))
    screen.blit(wallpaper,(0,0))
# ---------------------------------------------------------------------------
    # player movement
    playerX += playerX_change
    if playerX <= 0:
         playerX = 0 
    elif playerX >=536 :
        playerX = 536
# --------------------------------------------------------------------------
    # enemy movement
    for i in range(num_of_enemies):
        # game over check
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                gameover_display(gameoverx , gameovery)
                
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=536 :
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
# ------------------------------------------------------------------------------
        # bullet collision 
        collision = isCollision(enemyX[i] , enemyY[i] , bulletX , bulletY )
        if collision:
            bullet_state = 'ready'
            bulletY = 720
            score += 1
            enemyX[i] = random.randint(100,400)
            enemyY[i] = random.randint(50,150)
            collision_sound = mixer.Sound("F:\other\SPACE WAR GAME\explosion.wav")
            collision_sound.play()

        enemy(enemyX[i],enemyY[i],i)
# ----------------------------------------------------------------------------------
    # bullet movement 
    if bullet_state is 'fire':
        if bulletY <= 0 : 
            bullet_state = 'ready'
            bulletY = 720
        
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)
    score_display(scorex , scorey)
    pygame.display.update()
    