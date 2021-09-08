# Copyright: Thomas Oakes 2021
# Space Invaders
# This is Space Invaders created using pygame library
# This code was inspired by attreyabhatt's tutorial on github
# His version can be found at https://github.com/attreyabhatt/Space-Invaders-Pygame
# Icons from www.flaticon.com/
# Background image from www.freepik.com/
import random
import math
import pygame
from pygame import mixer

#initialize pygame
pygame.init()

#creates the screen
screen = pygame.display.set_mode((800,600))

#titel and icon change
pygame.display.set_caption("Space Invaders")
#go to flaticon.com or and look for an icon or make an icon to import into the project
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#background image
background = pygame.image.load('background.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('ufo.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0          #not used

#Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

#Creates num_of_enemies enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 732))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)

# Bullet
# Ready - you can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0         # not used
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True,(255,255,255))  
    screen.blit(game_over_text, (200, 250))

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(255,255,255))    
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 32,y + 10))   # The +16 is to shoot the bullet from the center, and the +10 is to have the bullet start from the top of the space ship 
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
# Game loop
running = True
while running:
    # This is an RGB value
    screen.fill((0,0,0))
    # Background image
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # If keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            elif event.key == pygame.K_UP:
                playerY_change = -0.3
            elif event.key == pygame.K_DOWN:
                playerY_change = 0.3
            elif event.key == pygame.K_SPACE:
                # Can only shoot a bullet in the ready state, other wise the bullet's X coordinate will change to the current space ship x coordinate
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Gets the space ship's X coordinate at the time that it is fired so that it doesn't move with the space ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    
    playerX += playerX_change
    
    # Creating outer bounds for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 732:
        playerX = 732
        
    # Enemy movement
    for i in range(num_of_enemies):
    
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 732:
            enemyX[i] = 732
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
            
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 732)
            enemyY[i] = random.randint(50, 150)
            
        enemy(enemyX[i], enemyY[i], i)
        
    # Bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -=bulletY_change
        
    # Checks to see if enemy has reached the player
    # If enemyY >= 480:
        

    # For up and down movement, but there isn't any in this game
    # PlayerY += playerY_change
    # Draws player after drawing the screen, otherwise the player will be drawn under the screen (background) layer
    player(playerX, playerY) #displayes the player in playerX, playerY locations
    show_score(textX, textY)
    pygame.display.update()