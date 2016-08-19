import zmq
from mm_server.matchmaker import Matchmaker

from server_common import config, mpwp_protocol as mpwp


class MatchmakerServer(object):
    router_sock = None
    address = None
    matchmaker = None
    io_loop = None

    def __init__(self, addr="tcp://*:", port=config.MATCHMAKER_PORT):
        super(MatchmakerServer, self).__init__()

        self.context = zmq.Context()
        self.io_loop = zmq.Poller()

        self.router_sock = self.context.socket(zmq.ROUTER)
        self.address = addr + str(port)
        self.router_sock.bind(self.address)

        self.dealer_sock = self.context.socket(zmq.DEALER)
        self.dealer_sock.connect(config.GAME_MANAGER_ADDR)
        self.dealer_sock.setsockopt(zmq.IDENTITY, mpwp.MATCHMAKER_ID)

        # self.router_sock = ZMQStream(self.router_sock)
        self.io_loop.register(self.router_sock, zmq.POLLIN)
        # self.router_sock.on_recv(self.recv)

        self.matchmaker = Matchmaker(self.send, self.create_game_cb)

    def start(self):
        while True:
            try:
                # self.io_loop.start()
                items = dict(self.io_loop.poll(0))
                if self.router_sock in items:
                    msg = self.router_sock.recv_multipart()
                    self.recv(msg)

            except Exception:
                break

        self.router_sock.close()
        self.dealer_sock.close()

    def create_game_cb(self, msg):
        self.dealer_sock.send_multipart(msg)
        # TODO: really need to make sure this doesnt hang forever
        rep = self.dealer_sock.recv_multipart()
        gid = rep[mpwp.MSG_CONTENT]
        return gid

    def send(self, msg):
        routable_msg = [msg[mpwp.MSG_TO]] + msg  # prepend routing IDENTITY
        self.router_sock.send_multipart(routable_msg)

    def recv(self, msg):
        if msg:
            router_id = msg[0]
            actual_msg = msg[1:]  # trim off router info
            if router_id == actual_msg[mpwp.MSG_FROM]:
                if actual_msg[mpwp.MSG_VERSION] == mpwp.VERSION:
                    if actual_msg[mpwp.MSG_TO] == mpwp.MATCHMAKER_ID:
                        if actual_msg[mpwp.MSG_STATUS] == mpwp.STATUS_OK:
                            sender_id = actual_msg[mpwp.MSG_FROM]
                            msg_type = actual_msg[mpwp.MSG_TYPE]
                            msg_content = mpwp.msg_content(actual_msg)
                            self.matchmaker.recv(sender_id, msg_type, msg_content)
                        else:
                            pass  # INVALID_RECEIVER_ERROR
                    else:
                        pass  # INVALID_STATUS_ERROR
                else:
                    pass  # send VERSION_MISMATCH_ERROR
            else:
                pass  # if IDENTITY not set correctly, send ZMQ_IDENTITY_ERROR
        else:
            return  # fatal error


def main():
    server = MatchmakerServer()
    server.start()


if __name__ == "__main__":
    main()
