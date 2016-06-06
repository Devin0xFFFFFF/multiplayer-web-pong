class GameObject(object):
    ID = None
    commands = None

    def __init__(self, id):
        self.ID = id
        self.commands = []

    def init(self, args):
        pass

    def update(self, delta):
        pass

    def act(self):
        pass

    def queue_command(self, command):
        self.commands.append(command)
