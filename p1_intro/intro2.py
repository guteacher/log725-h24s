import pygame
import sys
from src.cercle import Cercle

# Constants
WIDTH = 800
HEIGHT = 480

pygame.init()
clock = pygame.time.Clock()
clock.tick(60)
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
cercle = Cercle((255,0,0))


def gererFermeture():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

while True:
    gererFermeture()
    cercle.verifierX(ecran)
    
