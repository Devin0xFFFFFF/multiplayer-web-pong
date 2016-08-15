import zmq


class MatchmakerServer(object):
    ctx = None
    router_sock = None
    address = None

    def __init__(self, addr="tcp://*:", port=5555):
        super(MatchmakerServer, self).__init__()

        self.ctx = zmq.Context()

        self.router_sock = self.ctx.socket(zmq.ROUTER)
        self.address = addr + str(port)
        self.router_sock.bind(self.address)

    def start(self):
        pass

    def request_create_game(self, cid1, cid2):
        return b'0'


def main():
    server = MatchmakerServer()
    server.start()


if __name__ == "__main__":
    main()
