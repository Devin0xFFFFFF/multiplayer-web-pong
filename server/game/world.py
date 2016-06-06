from game.ball import Ball
from game.paddle import Paddle
from game_core.game import Game


class World(Game):
    ball = None
    paddle1 = None
    paddle2 = None

    count = 0

    def __init__(self, width, height):
        super(World, self).__init__(width, height)

        self.setup()
        print(self.paddle1.get_bounding_box())
        print(self.paddle2.get_bounding_box())
        print(self.ball.get_bounding_box())
        self.print_state()

    def setup(self):
        self.ball = Ball("ball", 50, 50)
        self.add_actor(self.ball, self.width / 2, self.height / 2)

        self.paddle1 = Paddle("paddle1", 20, 200)
        self.add_actor(self.paddle1, 20, self.height / 2)

        self.paddle2 = Paddle("paddle2", 20, 200)
        self.add_actor(self.paddle2, self.width - 20, self.height / 2)

    def act(self):
        if self.ball.intersecting(self.paddle1) or self.ball.intersecting(self.paddle2):
            self.ball.bounce(0)
        elif self.ball.at_game_left_edge():
            self.paddle1.score += 1
            self.ball.reset()
        elif self.ball.at_game_right_edge():
            self.paddle2.score += 1
            self.ball.reset()

        self.count += 1
        if self.count > 20:
            self.print_state()
            self.count = 0

    def print_state(self):
        for y in range(0, self.height):
                if y % 20 == 0:
                    for x in range(0, self.width):
                        if x % 5 == 0:
                            if self.paddle1.intersecting_position(x, y):
                                print("|", end="")
                            elif self.paddle2.intersecting_position(x, y):
                                print("I", end="")
                            elif self.ball.intersecting_position(x, y):
                                print("@", end="")
                            else:
                                print("-", end="")
                    print("")
