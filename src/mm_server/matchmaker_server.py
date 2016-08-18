import zmq
from mm_server.matchmaker import Matchmaker

from server_common import config, mpwp_protocol as mpwp

from zmq.eventloop.ioloop import IOLoop, PeriodicCallback
from zmq.eventloop.zmqstream import ZMQStream


class MatchmakerServer(object):
    router_sock = None
    address = None
    matchmaker = None
    io_loop = None

    def __init__(self, addr="tcp://*:", port=config.MATCHMAKER_PORT):
        super(MatchmakerServer, self).__init__()

        self.context = zmq.Context()
        self.io_loop = IOLoop.instance()

        self.router_sock = self.context.socket(zmq.ROUTER)
        self.address = addr + str(port)
        self.router_sock.bind(self.address)

        self.router_sock = ZMQStream(self.router_sock)
        self.router_sock.on_recv(self.recv)

        self.matchmaker = Matchmaker(self.send, self.request_create_game_cb)

    def start(self):
        try:
            self.io_loop.start()
        except KeyboardInterrupt:
            pass

        self.router_sock.close()

    def request_create_game_cb(self, msg):
        req_sock = self.context.socket(zmq.REQ)
        req_sock.send_multipart(msg)
        rep = req_sock.recv_multipart()
        return rep

    def send(self, msg):
        routable_msg = msg[mpwp.MSG_TO] + msg  # prepend routing IDENTITY
        self.router_sock.send_multipart(routable_msg)

    def recv(self, msg):
        if msg:
            router_id = msg[0]
            actual_msg = msg[1:]  # trim off router info
            if router_id == actual_msg[mpwp.MSG_FROM]:
                if msg[mpwp.MSG_VERSION] == mpwp.VERSION:
                    if msg[mpwp.MSG_TO] == mpwp.MATCHMAKER_ID:
                        if msg[mpwp.MSG_STATUS] == mpwp.STATUS_OK:
                            sender_id = msg[mpwp.MSG_FROM]
                            msg_type = msg[mpwp.MSG_TYPE]
                            msg_content = mpwp.msg_content(msg)
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
