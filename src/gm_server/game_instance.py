import threading
import zmq
import time
from game.pong_game.world import World
from server_common import mpwp_protocol, config


class GameInstance(threading.Thread):
    WORLD_WIDTH = 800
    WORLD_HEIGHT = 600

    GID = None  # Game ID
    clients = None  # List of clients in the game
    context = None
    dealer_sock = None
    game_world = None  # Game thread
    connected = True
    running = False
    update_time = 0
    unprocessed_commands = None
    poller = None

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super().__init__(group=group, target=target,
                         name=name)

        self.setDaemon(True)  # exit when manager exits
        self.args = args
        self.kwargs = kwargs

        self.GID = mpwp_protocol.get_uuid()
        self.clients = args

        self.context = zmq.Context()
        self.dealer_sock = self.context.socket(zmq.DEALER)
        self.dealer_sock.setsockopt(zmq.IDENTITY, self.GID)

        self.poller = zmq.Poller()
        self.poller.register(self.dealer_sock, zmq.POLLIN)

        self.game_world = World(self.WORLD_WIDTH, self.WORLD_HEIGHT)

        self.unprocessed_commands = []

    def connect_to_manager(self):
        self.dealer_sock.connect(config.GAME_MANAGER_ADDR_INTERNAL)

        msg = mpwp_protocol.get_mpwp_status_packet(mpwp_protocol.STATUS_CONNECT,
                                                   mpwp_protocol.GAME_MANAGER_ID,
                                                   self.GID)
        self.dealer_sock.send_multipart(msg)

        # could get stuck forever here if msg fails

        rep = self.dealer_sock.recv_multipart()

        return rep[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_CONNECT_OK

    def run(self):
        if self.connect_to_manager():
            self.connected = True
            while True:
                if self.connect_players():  # TODO: add code for game and connecting clients
                    self.running = True
                    self.run_game()
        else:
            return  # never got response, game failed to connect!

    def connect_players(self):
        # need a timeout here as well
        connected_clients = []
        for client in self.clients:  # expect all clients to respond
            msg = self.dealer_sock.recv_multipart()
            if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_CONNECT:
                cid = msg[mpwp_protocol.MSG_FROM]
                connected_clients.append(cid)
            else:
                return False  # bad message sent

        for client in connected_clients:  # all connected clients must be in the game
            if client not in self.clients:
                return False

        return True

    def run_game(self):
        last_time = time.clock()
        while self.running:
            self.recv_input()
            curr_time = time.clock()
            if curr_time - last_time > self.game_world.game_speed:
                last_time = curr_time
                self.game_world.step(self.unprocessed_commands)
                self.unprocessed_commands.clear()

    def recv_input(self):
        socks = dict(self.poller.poll(0))
        if socks.get(self.dealer_sock) == zmq.POLLIN:
            msg = self.dealer_sock.recv_multipart()
            if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_OK:
                if msg[mpwp_protocol.MSG_FROM] in self.clients:
                    trimmed_msg = msg[mpwp_protocol.MSG_FROM:]  # from, msgnum, type, content
                    self.unprocessed_commands.append(trimmed_msg)
                else:
                    pass  # invalid client!
            else:
                pass  # invalid status!
