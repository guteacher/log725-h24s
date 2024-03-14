import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_sprite = pygame.image.load('./assets/tank.png')
        self.current_sprite = self.base_sprite
        self.current_sprite = pygame.transform.rotate(self.base_sprite, 90)
        self.rect = self.current_sprite.get_rect()
        self.rect.center = (400, 500)
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
