import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, position_tuple):
        super().__init__()
        self.image = pygame.image.load('./assets/wall.png')
        self.rect = self.image.get_rect()
        self.rect.x = position_tuple[0]
        self.rect.y = position_tuple[1]
