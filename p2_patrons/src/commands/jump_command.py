from src.commands.command import Command


class JumpCommand(Command):

    def execute(self, actor):
        print("jump")
        actor.player.jump(actor.game_config['jump_sound'])
