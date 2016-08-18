from server_common.mpwp_data_sender import MPWPDataSender
from server_common import mpwp_protocol


from gm_server.game_instance import GameInstance


class GameManager(MPWPDataSender):
    games = None
    send_to_client_cb = None
    send_to_game_cb = None

    def __init__(self, send_to_client_cb, send_to_game_cb):
        self.games = {}
        self.send_to_client_cb = send_to_client_cb
        self.send_to_game_cb = send_to_game_cb

    def create_game(self, clients):
        game = GameInstance(args=clients)
        self.games[game.GID] = game
        game.start()
        return game

    def connect_game(self, GID):
        game = self.games[GID]
        msg = mpwp_protocol.get_mpwp_status_packet(mpwp_protocol.STATUS_CONNECT_OK,
                                                   GID,
                                                   mpwp_protocol.GAME_MANAGER_ID)
        self.send_to_game_cb(msg)
        self.alert_game_created(game)

    def recv_from_client(self, to_id, from_id, msg_type, msg_content):
        if to_id == mpwp_protocol.GAME_MANAGER_ID:
            if from_id == mpwp_protocol.MATCHMAKER_ID:
                self.handle_matchmaker_incoming(to_id, from_id, msg_type, msg_content)
            else:
                pass  # error, invalid sender!
        else:
            self.handle_client_incoming(to_id, from_id, msg_type, msg_content)

    def recv_from_game(self, msg):
        if msg[mpwp_protocol.MSG_TO] == mpwp_protocol.GAME_MANAGER_ID:
            self.handle_game_incoming(msg)
        else:
            self.send_to_client_cb(msg)

    def handle_client_incoming(self, to_id, from_id, msg_type, msg_content):
        gid = to_id
        cid = from_id
        if gid in self.games:
            game = self.games[gid]
            if cid in game.clients:
                game.forward_msg([msg_type] + msg_content)
            else:
                self.log(1, "Client '{}' does not exist in Game '{}'".format(cid, gid))
        else:
            self.log(1, "Game {} does not exist!".format(gid))

    def handle_matchmaker_incoming(self, to_id, from_id, msg_type, msg_content):
        if msg_type == mpwp_protocol.GAME_CREATE:
            clients = msg_content
            self.create_game(clients)
        else:
            pass  # invalid type!

    def handle_game_incoming(self, msg):
        if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_CONNECT:
            self.connect_game(msg[mpwp_protocol.MSG_FROM])
        elif msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_OK:
            game = self.games[msg[mpwp_protocol.MSG_FROM]]
            self.forward_to_all_clients(msg, game.clients)
        else:
            pass  # invalid status!

    def forward_to_all_clients(self, msg, clients):
        for client in clients:
            cli_msg = msg[:]
            cli_msg[mpwp_protocol.MSG_TO] = client  # the client ID
            self.send_to_client_cb(cli_msg)

    def alert_game_created(self, game):
        msg = self.get_packet(mpwp_protocol.MATCHMAKER_ID, mpwp_protocol.MATCHMAKER_LAUNCH, game.GID)
        self.forward_to_all_clients(msg, game.clients)
