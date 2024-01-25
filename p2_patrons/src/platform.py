import pygame
import math
from src.extracter import Extracter
from src.constants import CURRENT_W, CURRENT_H


class Platform(pygame.sprite.Sprite):
    extracter = Extracter()
    PERCENT_OF_SCREEN_HEIGHT = 0.07901234567901234
    GROUND_ADJUSTMENT = math.ceil(
        0.1111111111111111 * 0.07901234567901234 * CURRENT_H)
    TILESET_SIDELENGTH = 27
    scale_factor = PERCENT_OF_SCREEN_HEIGHT * CURRENT_H / TILESET_SIDELENGTH
    images = extracter.extract_platforms(scale_factor=scale_factor)
    images = {'left': images[0], 'centre': images[1], 'right': images[2]}

    def __init__(self, x, y, platform_type='centre'):
        super(Platform, self).__init__()
        # 16 is the height of the sprite in pixels
        self.image = self.images[platform_type.lower()]
        self.rect = self.image.get_rect()
        w, h = self.image.get_size()
        w -= self.GROUND_ADJUSTMENT * 2
        h -= self.GROUND_ADJUSTMENT
        self.collide_rect = pygame.rect.Rect((0, 0), (w, h))
        self.rect.topleft = (x, y)
        self.collide_rect.midbottom = self.rect.midbottom
