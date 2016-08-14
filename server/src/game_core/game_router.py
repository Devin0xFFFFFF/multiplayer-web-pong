from config import TYPE_COMMAND
from src.game_core.command import Command


class GameRouter(object):
    game = None

    def __init__(self, game):
        self.game = game

    def route_commands(self, commands):
        while commands:
            cid, msg_type, index, data = commands.pop(0)

            if msg_type == TYPE_COMMAND:
                self.route_command(cid, data)

    def route_command(self, cid, data):
        target_id, action, args = data

        player = self.game.get_player(cid)

        if player and player.owns_paddle(target_id):
            player.paddle.queue_command(Command(target_id, action, args))
        else:
            print("Invalid Command!")
