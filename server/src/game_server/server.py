import uuid


class Server(object):
    VERSION = b'mpwp0.1'

    STATUS_OK = b'100'
    STATUS_CONNECT = b'101'
    STATUS_DISCONNECT = b'102'
    STATUS_CONFIRM = b'103'
    STATUS_CREATE = b'104'
    STATUS_CREATED = b'105'
    STATUS_READY = b'106'

    STATUS_FAIL = b'500'

    clients = None

    def __init__(self):
        self.clients = []

    @staticmethod
    def get_uuid():
        return uuid.uuid4()
