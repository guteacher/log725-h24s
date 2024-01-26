import pygame
from src.commands.command import Command


class OpenMenuCommand(Command):

    def execute(self, actor):
        pygame.mixer.Channel(0).pause()
        actor.music_playing = False
        if actor.pause_menu(actor.player) == 'Main Menu':
            return -1
        else:
            actor.hide_mouse()
        if actor.game_config['background_music']:
            pygame.mixer.Channel(0).unpause()
            actor.music_playing = True
