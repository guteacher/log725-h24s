import pygame
import sys

# Constants
WIDTH = 800
HEIGHT = 480

pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
tableSprite = pygame.image.load("images/table.png")
squareSprite = pygame.image.load("images/square.png")

def gererFermeture():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

while True:
    gererFermeture()
    ecran.blit(tableSprite, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL] and keys[pygame.K_x]:
        ecran.blit(squareSprite, (250, 250))

    pygame.draw.circle(ecran, (255, 0, 0), (50, 50), 10)
    pygame.draw.rect(ecran, (0, 0, 255), (0,0,100,100))

    pygame.display.flip()