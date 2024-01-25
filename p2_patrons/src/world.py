import pygame
import math
import random
from src.player import Player
from src.platform import Platform
from src.constants import CURRENT_W, CURRENT_H


class World:
    P_PLATFORM = 0.8  # probability of platforms
    previous_platform_seed = [0, 0]
    difficulty = 1

    def __init__(self, max_gaps):
        TILESET_SIDELENGTH = Platform.TILESET_SIDELENGTH
        self.platform_list = pygame.sprite.Group()
        self.player = None
        self.screen_width, self.screen_height = CURRENT_W, CURRENT_H
        self.scale_factor = 0.07901234567901234 * CURRENT_H / TILESET_SIDELENGTH
        self.tileset_new_sidelength = int(
            TILESET_SIDELENGTH * self.scale_factor)
        self.number_of_spots = self.screen_width // self.tileset_new_sidelength
        self.max_gaps = max_gaps
        pos_y = self.screen_height - self.tileset_new_sidelength
        for pos_x in range(0, self.screen_width, self.tileset_new_sidelength):
            platform = Platform(pos_x, pos_y)
            self.platform_list.add(platform)
        for x in range(3, math.ceil(self.screen_height / self.tileset_new_sidelength), 3):
            self.create_platforms(self.screen_height -
                                  self.tileset_new_sidelength * (x + 1))

    def draw(self, screen):
        self.platform_list.draw(screen)

    def set_player(self, player: Player):
        player.rect.bottom = CURRENT_H - \
            self.tileset_new_sidelength + player.GROUND_ADJUSTMENT
        player.rect.right = CURRENT_W / 2
        player.collide_rect.midbottom = player.rect.midbottom
        self.player = player

    def create_platforms(self, pos_y):
        num_platforms = max(
            ((self.screen_width) // self.tileset_new_sidelength), 2)
        limit_for_gap = num_platforms - 5
        gap_pos = []
        print(self.max_gaps)
        if self.max_gaps == 2:
            gap_pos.append(random.randint(2, limit_for_gap))
            gap_pos.append(gap_pos[0] + 5)
        else:
            gap_pos.append(random.randint(2, limit_for_gap))

        if gap_pos[0] == self.previous_platform_seed:
            if gap_pos[0] > 5:
                gap_pos[0] = gap_pos[0] - 2
                if self.max_gaps == 2:
                    gap_pos[1] = gap_pos[1] - 2
            else:
                gap_pos[0] = gap_pos[0] + 2
                if self.max_gaps == 2:
                    gap_pos[1] = gap_pos[1] + 2

        i = 0
        for platform in range(num_platforms):
            if pos_y == 412:
                if (i in [5, 6]):
                    i += 1
                    continue
                else:
                    platform = Platform(platform * 47, pos_y, 'centre')
                    self.platform_list.add(platform)
                i += 1
                self.previous_platform_seed = 5
            else:
                if platform == gap_pos[0] or platform == gap_pos[0] + 1:
                    continue
                if self.max_gaps == 2:
                    if platform == gap_pos[1] or platform == gap_pos[1] + 1:
                        continue
                platform = Platform(platform * 47, pos_y, 'centre')
                self.platform_list.add(platform)
                self.previous_platform_seed = gap_pos[0]

    def shift_world(self, shift_y=0, shift_x=0):
        """For automated scrolling"""
        platforms_to_remove = []
        highest_y = self.screen_height
        # Shift player
        self.player.rect.y += shift_y
        self.player.rect.x += shift_x
        self.player.collide_rect.y += shift_y
        self.player.collide_rect.x += shift_x

        # Shift platforms
        for platform in self.platform_list:
            platform.rect.y += shift_y
            platform.collide_rect.y += shift_y
            platform.rect.x += shift_x
            platform.collide_rect.x += shift_x
            if platform.rect.y < highest_y:
                highest_y = platform.rect.y
            if platform.rect.top > self.screen_height + self.player.rect.height:
                platforms_to_remove.append(platform)
        # remove platforms that are out of bounds
        if platforms_to_remove:
            self.platform_list.remove(platforms_to_remove)
            platforms_to_remove.clear()
        # create new platforms
        if highest_y > -self.tileset_new_sidelength * 3:  # Buffer
            self.create_platforms(highest_y - self.tileset_new_sidelength * 3)

    def update(self):
        self.platform_list.update()
