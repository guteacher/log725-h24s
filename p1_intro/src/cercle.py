import pygame
from src.forme import Forme

class Cercle(Forme):
    rayon = 10

    def __init__(self, couleur):
        Forme.__init__(self, couleur)

    def retournerOriginal(self):
        if self.rayon > 10:
            self.rayon -= 1
        else:
            self.rayon = 10

    def verifierX(self, ecran):
        self.verifierEspace()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            self.rayon += 1
        else:
            self.retournerOriginal()
        pygame.draw.circle(ecran, self.couleur, (200, 200), self.rayon, 0)
        pygame.display.flip()
        ecran.fill((0,0,0))