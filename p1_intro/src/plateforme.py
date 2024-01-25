import pygame
class Plateforme:
    couleur = (255, 0, 0)
    pos_x = 250
    pos_y = 250

    def __init__(self, couleur):
        self.couleur = couleur

    def dessiner(self, ecran):
        pygame.draw.rect(ecran, self.couleur, (self.pos_x, self.pos_y, 50, 200))

    def se_deplacer(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos_y -= 5
        if keys[pygame.K_DOWN]:
            self.pos_y += 5
