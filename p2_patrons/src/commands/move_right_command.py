from src.commands.command import Command


class MoveRightCommand(Command):

    def execute(self, actor):
        print("move right")
        actor.player.go_right()
