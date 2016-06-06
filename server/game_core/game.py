import timeit

import time

from game_core.game_object import GameObject


class Game(GameObject):
    router = None

    players = None
    actors = None

    width = None
    height = None

    game_speed = None
    last_timestamp = None

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.players = []
        self.actors = []

        self.game_speed = 20
        self.last_timestamp = 0.0

    def run(self):
        while True:
            time.sleep(self.game_speed / 1000)
            self.update(0)

    def init(self, command_router):
        self.router = command_router

    def add_player(self, player):
        self.players.append(player)

    def add_actor(self, actor, x=0, y=0):
        actor.game = self
        actor.set_position(x, y)
        self.actors.append(actor)

    def get_actor(self, actor_id):
        return next([x for x in self.actors if x.ID == actor_id], None)

    def update(self, delta):
        self.last_timestamp = delta

        for player in self.players:
            player.run()

        self.act()

        for actor in self.actors:
            actor.update(delta)

    def act(self):
        pass
