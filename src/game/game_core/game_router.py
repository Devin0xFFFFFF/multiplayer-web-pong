import json

from server_common import mpwp_protocol
from game.game_core.command import Command


class GameRouter(object):
    game = None

    def __init__(self, game):
        self.game = game

    def route_commands(self, commands):
        while commands:
            cid, index, msg_type, data = commands.pop(0)

            if msg_type == mpwp_protocol.GAME_INPUT:
                cmd = json.loads(data.decode())
                self.route_command(cid, cmd)

    def route_command(self, cid, cmd):
        target_id, action, args = cmd
        target_id = target_id.encode()

        player = self.game.get_player(cid)

        if player and player.owns_paddle(target_id):
            player.paddle.queue_command(Command(target_id, action, args))
        else:
            print("Invalid Command!")
