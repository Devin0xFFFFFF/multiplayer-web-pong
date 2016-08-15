from ..server_common.mpwp_data_sender import MPWPDataSender
from ..server_common import mpwp_protocol
from threading import Timer


class GameInstance():
    GID = None  # Game ID
    clients = None  # List of clients in the game
    pipe = None  # Pipe connecting to game thread
    game_thread = None  # Game thread

    def __init__(self, clients):
        self.GID = mpwp_protocol.get_uuid()
        self.clients = []
        # self.pipe = MockPipe()
        # init game thread

    def forward_msg(self, msg):
        self.pipe.send(msg)


class GameManager(MPWPDataSender):
    games = None
    socket = None

    def __init__(self, socket):
        self.games = {}
        self.socket = socket

    def create_game(self, clients):
        game = GameInstance(clients)
        self.games[game.GID] = game
        self.alert_game_created(game)

    def recv(self, msg):
        print(msg)
        if msg and msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_OK:
            data = mpwp_protocol.msg_data(msg)
            t = msg[mpwp_protocol.MSG_TO]
            f = msg[mpwp_protocol.MSG_FROM]
            if f == mpwp_protocol.MATCHMAKER_ID and t == mpwp_protocol.GAME_MANAGER_ID:
                self.handle_matchmaker_incoming(data)
            else:
                self.handle_client_incoming(t, f, data)

    def send(self, id, msg):
        return self.socket.send(id, msg)

    def handle_client_incoming(self, gid, cid, data):
        if gid in self.games:
            game = self.games[gid]
            if cid in game.clients:
                game.forward_msg(data)
            else:
                print("Client '{}' does not exist in Game '{}'".format(cid, gid))
        else:
            print("Game {} does not exist!".format(gid))

    def handle_matchmaker_incoming(self, data):
        cmd_type = data[1]
        clients = data[2]
        if cmd_type == mpwp_protocol.GAME_MANAGER_CREATE:
            self.create_game(clients)
        else:
            print("Invalid Message From Matchmaker!")

    def alert_game_created(self, game):
        msg = self.get_packet(mpwp_protocol.MATCHMAKER_ID, mpwp_protocol.MATCHMAKER_LAUNCH, "{}".format(game.GID))
        self.send(mpwp_protocol.MATCHMAKER_ID, msg)
