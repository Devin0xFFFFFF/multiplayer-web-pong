from game_core.actor import Actor


class Paddle(Actor):
    speed = None
    score = None

    def __init__(self, actor_id, width=0, height=0):
        super(Paddle, self).__init__(actor_id, width, height)

        self.score = 0

    def init(self, args):
        self.speed = 10

    def act(self):
        pass
