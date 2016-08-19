import zmq

from server_common import config, mpwp_protocol as mwp


class MockLogger(object):
    context = None
    sock = None
    address = None

    log_buffer = []
    log_buf_size = 100

    def __init__(self, addr="tcp://*:", port=config.LOGGER_PORT):
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.PULL)
        self.address = addr + str(port)
        self.sock.bind(self.address)

    def start(self):
        while True:
            msg = self.sock.recv_multipart()
            if msg[mwp.MSG_VERSION] == mwp.VERSION:
                if msg[mwp.MSG_STATUS] == mwp.STATUS_LOG:
                    if msg[mwp.MSG_TO] == mwp.LOGGER_ID:
                        self.log_msg(msg)
                    else:
                        print("TO_ID ERROR: {}".format(msg))
                else:
                    print("STATUS ERROR: {}".format(msg))
            else:
                print("VERSION ERROR: {}".format(msg))

    def log_msg(self, msg):
        log_lvl = int(msg[mwp.MSG_TYPE].decode())
        log_num = int(msg[mwp.MSG_MSGNUM].decode())
        log_from = "_" + msg[mwp.MSG_FROM].decode()
        log_content = msg[mwp.MSG_CONTENT]

        self.log_buffer.append(log_content)
        self.log_buffer = self.log_buffer[-self.log_buf_size:]

        print("{} @{} #{}:    {}".format(log_lvl, log_from, log_num, log_content))


def main():
    server = MockLogger()
    server.start()


if __name__ == "__main__":
    main()
