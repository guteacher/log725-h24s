import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./assets/tank.png')
        self.rect = self.current_sprite.get_rect()
        self.rect.center = (100, 500)
        self.speed = 6

    def update(self):
        pass
        # iterate over all bullets
        # if no bullets, or bullets too far, don't move
        # if the closest bullet is on the right, move to the left cover
        # if the closest bullet is on the left, move to the right cover
        # if in cover and no more bullets, move back to the center
        # if the enemy is being shot too frequently, take longer to leave cover and start running to cover sooner
