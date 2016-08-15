class Command(object):
    targetID = None
    action = None
    args = None

    def __init__(self, targetid, action, args=[]):
        if targetid and (isinstance(targetid, bytes) or isinstance(targetid, str)):
            self.targetID = targetid
        else:
            raise TypeError
        if action and isinstance(action, str):
            self.action = action
        else:
            raise TypeError
        if isinstance(args, list):
            self.args = args
        else:
            raise TypeError

    def execute(self, target):
        if target.ID == self.targetID:
            getattr(target, self.action)(*self.args)
        else:
            raise NameError

    def serialize(self):
        return [self.targetID, self.action, self.args]
