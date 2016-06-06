from game_core.game_commander import GameCommander


class Player(GameCommander):
    ID = None

    game = None
    paddle = None

    def __init__(self, player_id, paddle):
        self.ID = player_id
        self.paddle = paddle

    def run(self):
        pass
