import zmq
from gm_server.game_manager import GameManager

from server_common import config, mpwp_protocol as mpwp

from zmq.eventloop.ioloop import ZMQIOLoop
from zmq.eventloop.zmqstream import ZMQStream


class GameManagerServer(object):
    client_router_sock = None
    worker_router_sock = None
    address = None
    manager = None
    io_loop = None

    def __init__(self, addr="tcp://*:", port=config.GAME_MANAGER_PORT):
        super(GameManagerServer, self).__init__()

        self.context = zmq.Context()
        self.io_loop = ZMQIOLoop.instance()

        self.client_router_sock = self.context.socket(zmq.ROUTER)
        self.address = addr + str(port)
        self.client_router_sock.bind(self.address)

        self.worker_router_sock = self.context.socket(zmq.ROUTER)
        self.worker_router_sock.bind("tcp://*:6000")

        self.client_router_sock = ZMQStream(self.client_router_sock)
        self.client_router_sock.on_recv(self.recv_from_client)

        self.worker_router_sock = ZMQStream(self.worker_router_sock)
        self.worker_router_sock.on_recv(self.recv_from_game)

        self.manager = GameManager(self.send_to_client, self.send_to_game)

    def start(self):
        try:
            self.io_loop.start()
        except KeyboardInterrupt:
            pass

        self.client_router_sock.close()
        self.worker_router_sock.close()

    def send_to_client(self, msg):
        routable_msg = [msg[mpwp.MSG_TO]] + msg  # prepend routing IDENTITY
        self.client_router_sock.send_multipart(routable_msg)

    def send_to_game(self, msg):
        routable_msg = [msg[mpwp.MSG_TO]] + msg  # prepend routing IDENTITY
        self.worker_router_sock.send_multipart(routable_msg)

    def recv_from_client(self, msg):
        if msg:
            router_id = msg[0]
            actual_msg = msg[1:]  # trim off router info
            if router_id == actual_msg[mpwp.MSG_FROM]:
                if actual_msg[mpwp.MSG_VERSION] == mpwp.VERSION:
                    to_id = actual_msg[mpwp.MSG_TO]
                    from_id = actual_msg[mpwp.MSG_FROM]
                    msg_type = actual_msg[mpwp.MSG_TYPE]
                    msg_content = mpwp.msg_content(actual_msg)
                    self.manager.handle_client_incoming(to_id, from_id, msg_type, msg_content)
                else:
                    pass  # send VERSION_MISMATCH_ERROR
            else:
                if actual_msg[mpwp.MSG_TO] == mpwp.GAME_MANAGER_ID and actual_msg[mpwp.MSG_FROM] == mpwp.MATCHMAKER_ID:
                    to_id = router_id
                    from_id = actual_msg[mpwp.MSG_FROM]
                    msg_type = actual_msg[mpwp.MSG_TYPE]
                    msg_content = mpwp.msg_content(actual_msg)
                    self.manager.handle_matchmaker_incoming(to_id, from_id, msg_type, msg_content)
                else:
                    pass  # error, invalid message
        else:
            return  # fatal error

    def recv_from_game(self, msg):
        router_id = msg[0]
        actual_msg = msg[1:]  # trim off router info
        self.manager.recv_from_game(actual_msg)


def main():
    server = GameManagerServer()
    server.start()


if __name__ == "__main__":
    main()
