import uuid

# MSG PARTS FOR FLEXIBLE INDEXING

MSG_VERSION = 0
MSG_STATUS = 1
MSG_TO = 2
MSG_FROM = 3
MSG_MSGNUM = 4
MSG_TYPE = 5
MSG_CONTENT = 6

# VERSION TAG

VERSION = b'mpwp_v1.0'

# STATUS CODES

STATUS_DATA = b'100'
STATUS_PING = b'101'

STATUS_CONNECT = b'200'
STATUS_CONNECT_OK = b'201'
STATUS_DISCONNECT = b'202'
STATUS_REGISTER = b'203'
STATUS_REGISTER_OK = b'204'
STATUS_RESYNC = b'205'
STATUS_RESYNC_OK = b'206'

STATUS_LOG = b'300'

STATUS_SERVER_ERROR = b'500'
STATUS_VERSION_MISMATCH_ERROR = b'501'
STATUS_INCORRECT_ID_ERROR = b'502'

# SERVER IDS

MATCHMAKER_ID = b'0'
GAME_MANAGER_ID = b'1'
CLIENT_HANDLER_ID = b'2'
LOGGER_ID = b'3'

# GAME MSG TYPES

GAME_CREATE = b'0'
GAME_STATE = b'1'
GAME_INPUT = b'2'

# MATCHMAKER MSG TYPES

MATCHMAKER_QUEUE = b'0'
MATCHMAKER_DEQUEUE = b'1'
MATCHMAKER_FOUND = b'2'
MATCHMAKER_ACCEPT = b'3'
MATCHMAKER_DECLINE = b'4'
MATCHMAKER_LOADING = b'5'
MATCHMAKER_LAUNCH = b'6'
MATCHMAKER_SYNC = b'7'


def get_uuid():
    return ("{}".format(uuid.uuid1())).encode()


def get_mpwp_packet(STATUS, TO, FROM, MSGNUM, TYPE):
    return [VERSION, STATUS, TO, FROM, MSGNUM, TYPE]


def get_mpwp_status_packet(STATUS, TO, FROM):
    return [VERSION, STATUS, TO, FROM]


def get_mpwp_content_packet(TO, FROM, MSGNUM, TYPE, CONTENT=None):
    packet = get_mpwp_packet(STATUS_DATA, TO, FROM, MSGNUM, TYPE)
    if CONTENT:
        if type(CONTENT) == list:
            packet = packet + CONTENT
        elif type(CONTENT) is bytes:
            packet.append(CONTENT)
        else:
            raise TypeError
    return packet


def get_log_packet(FROM, MSGNUM, TYPE, MSG=b''):
    packet = [VERSION, STATUS_LOG, LOGGER_ID, FROM, MSGNUM, TYPE, MSG]
    return packet


def msg_content(msg):
    return msg[MSG_CONTENT:]
