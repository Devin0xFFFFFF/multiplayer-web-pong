import uuid

MSG_VERSION = 0
MSG_STATUS = 1
MSG_TO = 2
MSG_FROM = 3
MSG_BODY = 4

VERSION = "mpwp_v1.0"

STATUS_OK = b'100'
STATUS_CONNECT = b'101'
STATUS_DISCONNECT = b'102'
STATUS_CONFIRM = b'103'
STATUS_CREATE = b'104'
STATUS_CREATED = b'105'
STATUS_READY = b'106'

STATUS_FAIL = b'500'

MATCHMAKER_ID = b'0'
GAME_MANAGER_ID = b'1'

GAME_CREATE = 0
GAME_STATE = 1
GAME_INPUT = 2

MATCHMAKER_QUEUE = 0
MATCHMAKER_DEQUEUE = 1
MATCHMAKER_FOUND = 2
MATCHMAKER_ACCEPT = 3
MATCHMAKER_DECLINE = 4
MATCHMAKER_LOADING = 5
MATCHMAKER_LAUNCH = 6
MATCHMAKER_SYNC = 7


def get_uuid():
    return ("{}".format(uuid.uuid4())).encode()


def get_mpwp_packet(STATUS, TO, FROM, BODY):
    # MSG = [HEAD(VERSION, STATUS, TO, FROM), BODY(%s)]
    return [VERSION, STATUS, TO, FROM, BODY]


def get_mpwp_data_packet(TO, FROM, DATA):
    return get_mpwp_packet(STATUS_OK, TO, FROM, {'data': DATA})


def serialize_packet(packet):
    return packet


def msg_data(msg):
    return msg[MSG_BODY]['data']
