from .game_commander import GameCommander


class Player(GameCommander):
    ID = None

    game = None
    paddle = None

    def __init__(self, player_id, paddle):
        self.ID = player_id
        self.paddle = paddle

    def run(self):
        pass

    def owns_paddle(self, paddle_id):
        return self.paddle.ID == paddle_id

    def set_client(self, cid):
        self.ID = cid
