import sys
from src.commands.command import Command


class QuitCommand(Command):

    def execute(self, actor):
        print("quitter")
        sys.exit()
