class Command(object):
    targetID = None
    action = None
    args = None

    def __init__(self, targetid, action, args=[]):
        self.targetID = targetid
        self.action = action
        self.args = args

    def execute(self, target):
        getattr(target, self.action)(self.args)

    def serialize(self):
        return [self.targetID, self.action, self.args]
