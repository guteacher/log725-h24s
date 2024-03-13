import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load('./assets/wall.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
