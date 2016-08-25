import threading
import zmq
import time
import json
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
    state_count = None
    matchmaker_alias = None
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
        self.state_count = 0

        self.unprocessed_commands = []

    def send_register_ok(self, cid):
        packet = mpwp_protocol.get_mpwp_status_packet(mpwp_protocol.STATUS_REGISTER_OK,
                                                      cid,
                                                      self.GID)

        self.dealer_sock.send_multipart(packet)

    def connect_to_manager(self):
        self.dealer_sock.connect("tcp://localhost:6000")

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
        # TODO: make this fault tolerant with a Timer
        for client in self.clients:  # expect all clients to respond
            msg = self.dealer_sock.recv_multipart()
            if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_REGISTER:
                cid = msg[mpwp_protocol.MSG_FROM]
                connected_clients.append(cid)
                self.send_register_ok(cid)
            else:
                return False  # bad message sent

        for idx, client in enumerate(connected_clients):  # all connected clients must be in the game
            if client not in self.clients:
                return False
            else:
                self.game_world.players[idx].set_client(client)

        return True

    def run_game(self):
        last_time = time.clock()
        while self.running:
            self.recv_input()
            curr_time = time.clock()
            if curr_time - last_time > self.game_world.game_speed/1000:
                last_time = curr_time
                self.game_world.step(self.unprocessed_commands)
                self.unprocessed_commands.clear()
                self.push_state()

    def push_state(self):
        game_state = self.game_world.get_state()
        packed_state = json.dumps(game_state).encode()
        packet = mpwp_protocol.get_mpwp_content_packet(mpwp_protocol.GAME_MANAGER_ID,
                                                       self.GID,
                                                       str(self.state_count).encode(),
                                                       mpwp_protocol.GAME_STATE,
                                                       packed_state)
        self.dealer_sock.send_multipart(packet)

    def recv_input(self):
        socks = dict(self.poller.poll(0))
        if socks.get(self.dealer_sock) == zmq.POLLIN:
            msg = self.dealer_sock.recv_multipart()
            if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_DATA:
                if msg[mpwp_protocol.MSG_FROM] in self.clients:
                    trimmed_msg = msg[mpwp_protocol.MSG_FROM:]  # from, msgnum, type, content
                    self.unprocessed_commands.append(trimmed_msg)
                else:
                    pass  # invalid client!
            else:
                pass  # invalid status!
