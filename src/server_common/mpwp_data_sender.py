import zmq
import json

from server_common import mpwp_protocol, config


class MPWPDataSender(object):
    ID = None
    MSGNUM = 0
    context = None

    log_sock = None
    log_level = 0
    LOGNUM = 0

    def __init__(self, log_level=1):
        self.context = zmq.Context()

        self.log_level = log_level
        if self.log_level > 0:
            self.log_sock = self.context.socket(zmq.PUSH)
            self.log_sock.connect(config.LOGGER_ADDR)

    def assign_id(self):
        self.ID = mpwp_protocol.get_uuid()

    def get_packet(self, TO, TYPE, CONTENT=None):
        packet = mpwp_protocol.get_mpwp_content_packet(TO, self.ID, str(self.MSGNUM).encode(), TYPE, CONTENT)
        self.MSGNUM += 1
        return packet

    def log(self, log_level, log_msg):
        if self.log_level and log_level >= self.log_level:
            packet = mpwp_protocol.get_log_packet(self.ID, str(self.LOGNUM).encode(),
                                                  str(log_level).encode(), str(log_msg).encode())
            self.LOGNUM += 1
            print(packet)
            self.log_sock.send_multipart(packet)
