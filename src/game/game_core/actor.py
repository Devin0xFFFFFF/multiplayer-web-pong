import math

from .game_object import GameObject
from .physics.point import Point

from .physics.rectangle import Rectangle


class Actor(GameObject):
    game = None

    x = None
    y = None
    width = None
    height = None
    rotation = None
    visible = None

    collisionBuffer = None

    def __init__(self, actor_id, width=0, height=0):
        super(Actor, self).__init__(actor_id)

        self.visible = True
        self.collisionBuffer = 10

        self.x = 0
        self.y = 0

        if isinstance(width, int):
            self.width = width
        else:
            raise TypeError
        if isinstance(height, int):
            self.height = height
        else:
            raise TypeError

        self.rotation = 0

    def update(self, delta):
        while self.commands:
            cmd = self.commands.pop(0)

            cmd.execute(self)

        self.act()

    def act(self):
        pass

    def send_command(self, action, args):
        pass

    def get_state(self):
        return [self.visible, self.x, self.y, self.width, self.height, self.rotation]

    def set_position(self, x=0, y=0):
        if isinstance(x, int):
            self.x = x
        elif isinstance(x, float):
            self.x = math.trunc(x)
        else:
            raise TypeError

        if isinstance(y, int):
            self.y = y
        elif isinstance(y, float):
            self.y = math.trunc(y)
        else:
            raise TypeError

    def set_rotation(self, angle):
        if isinstance(angle, int):
            self.rotation = angle % 360
        else:
            raise TypeError

    def move(self, speed=1):
        angle = self.rotation * (math.pi / 180.0)
        x = math.trunc((self.x + math.cos(angle) * speed))
        y = math.trunc((self.y + math.sin(angle) * speed))

        self.set_position(x, y)

    def get_bounding_box(self):
        return Rectangle(Point(self.x - self.collisionBuffer, self.y - self.collisionBuffer),
                         Point(self.x + self.width + self.collisionBuffer, self.y + self.height + self.collisionBuffer))

    def intersecting(self, actor):
        return self.get_bounding_box().overlaps(actor.get_bounding_box())

    def intersecting_position(self, x, y):
        return self.get_bounding_box().contains(Point(x, y))

    def at_game_top_edge(self):
        return self.y < self.collisionBuffer

    def at_game_bottom_edge(self):
        return self.y + self.height > self.game.height - self.collisionBuffer

    def at_game_left_edge(self):
        return self.x < self.collisionBuffer

    def at_game_right_edge(self):
        return self.x + self.width > self.game.width - self.collisionBuffer
