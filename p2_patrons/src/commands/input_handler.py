
import pygame
import sys
from src.commands.jump_command import JumpCommand
from src.commands.move_left_command import MoveLeftCommand
from src.commands.move_right_command import MoveRightCommand
from src.commands.open_menu_command import OpenMenuCommand
from src.commands.quit_command import QuitCommand
from pygame import K_UP, K_LEFT, K_RIGHT, K_ESCAPE, K_F4, K_LALT, K_RALT, QUIT, KEYUP, KEYDOWN


class InputHandler:

    k_up_ = JumpCommand()
    k_left_ = MoveLeftCommand()
    k_right_ = MoveRightCommand()
    k_escape_ = OpenMenuCommand()
    k_alt_f4_ = QuitCommand()

    def handle(self, actor):
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()

            alt_f4 = (event.type == KEYDOWN and event.key == K_F4
                      and (pressed_keys[K_LALT] or pressed_keys[K_RALT]))

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.k_left_.execute(actor)
                elif event.key == K_RIGHT:
                    self.k_right_.execute(actor)
                elif event.key == K_UP:
                    self.k_up_.execute(actor)
                elif event.key == K_ESCAPE:
                    self.k_escape_.execute(actor)

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    actor.player.stop(pressed_keys)

            if event.type == QUIT or alt_f4:
                self.k_alt_f4_.execute(actor)
