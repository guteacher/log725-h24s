from src.commands.command import Command


class MoveLeftCommand(Command):

    def execute(self, actor):
        print("move left")
        actor.player.go_left()
