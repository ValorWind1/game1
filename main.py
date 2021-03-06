import pygame
from pygame import mixer
import random
import math



# initializes the pygame
pygame.init()

# create screen + size of screen W X H
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('f45851c2e013d2d4a8df3b1b47eb87d6.png')

# Background Sound
mixer.music.load('backgroundMusic.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("*Space*")
icon = pygame.image.load('happyearth.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('battleship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Player Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numberOfEnemies = 6

for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load('ufo .png'))
    enemyX.append (random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append ((2))
    enemyY_change.append ((40))

# Bullet
# ready - cant see bullet on screen
# Fire the bullet is currently moving

bulletImg = pygame.image.load('bullets.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('YR.otf' , 40)
textX = 10
textY = 10

#Game over Text
over_font = pygame.font.Font('High Summit.ttf' , 64)

def game_over_text():
    over_text = over_font.render("GAME  OVER " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255) )
    screen.blit(score, (x,y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop so screen doesnt close down
running = True
while running:

    # color window
    screen.fill((0, 25, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed checked whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('Cannon-SoundBible.com-1661203605.wav')
                    bullet_Sound.play()
                    # get current x cordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for bounderies for spaceship so it wont go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(numberOfEnemies):

        #GAME OVER
        if enemyY[i] > 440:
            for j in range(numberOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exlposion_Sound = mixer.Sound('Blast-SoundBible.com-2068539061.wav')
            exlposion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
