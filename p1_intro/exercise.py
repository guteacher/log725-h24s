import pgzrun
import pygame
from src.plateforme import Plateforme

# Constants
WIDTH = 800
HEIGHT = 480

ecran = pygame.display.set_mode()
tableSprite = pygame.image.load("images/table.png")
plat = Plateforme((0, 255, 0))

def update():
    area = ecran.get_rect()
    ecran.blit(tableSprite, (0, 0))
    plat.dessiner(ecran)
    plat.se_deplacer()
    
# Start
pgzrun.go()
