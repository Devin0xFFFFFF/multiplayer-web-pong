class GameObject(object):
    ID = None
    commands = None

    def __init__(self, obj_id):
        if isinstance(obj_id, bytes):
            self.ID = obj_id
        else:
            raise TypeError

        self.commands = []

    def init(self, args):
        pass

    def update(self, delta):
        pass

    def act(self):
        pass

    def get_state(self):
        pass

    def queue_command(self, command):
        self.commands.append(command)
