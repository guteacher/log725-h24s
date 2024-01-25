import pygame

class Forme:
    couleur = (255, 0, 0)

    def __init__(self, couleur):
        self.couleur = couleur

    def verifierEspace(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.couleur = (0, 255, 0)
        else:
            self.couleur = (255, 0, 0)