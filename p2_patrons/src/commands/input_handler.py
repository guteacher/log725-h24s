import pygame
from pygame import (
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_F4,
    K_LALT,
    K_RALT,
    QUIT,
    KEYUP,
    KEYDOWN,
)


class InputHandler:
    # créer les instances des Commands

    def handle(self, actor):
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()

            if event.type == KEYDOWN:
                # si une telle touche est apuyée, appelez tel Command 
                pass

            if event.type == KEYUP:
                pass

            if event.type == QUIT or alt_f4:
                pass
