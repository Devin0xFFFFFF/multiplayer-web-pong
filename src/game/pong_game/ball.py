from random import random

from src.game_core.actor import Actor


class Ball(Actor):
    speed = None

    def __init__(self, actor_id, width=0, height=0):
        super(Ball, self).__init__(actor_id, width, height)

        self.speed = 10

    def act(self):
        self.move(self.speed)

        if self.at_game_top_edge() or self.at_game_bottom_edge():
            self.bounce()

    def get_state(self):
        return super(Ball, self).get_state()

    def bounce(self, variance=0):
        self.set_rotation(self.rotation + 270 + variance)
        # print("Bounce at {0} {1}".format(self.x, self.y))

    def randomize_direction(self):
        rand = random.randint(0, 45)
        rand_dir = random.randint(0, 3)

        if rand_dir == 0:
            self.set_rotation(rand)
        elif rand_dir == 1:
            self.set_rotation(180 - rand)
        elif rand_dir == 2:
            self.set_rotation(180 + rand)
        elif rand_dir == 3:
            self.set_rotation(360 - rand)

    def reset(self):
        self.set_position(self.game.width / 2, self.game.height / 2)
