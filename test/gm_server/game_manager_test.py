import unittest

from gm_server.game_manager import GameManager


class GameManager_testCase(unittest.TestCase):
    mock_outgoing_client_buffer = []
    mock_outgoing_game_buffer = []

    def setUp(self):
        self.gm = GameManager(self.mock_send_to_client_cb, self.mock_send_to_game_cb)

    def tearDown(self):
        self.gm = None
        self.mock_outgoing_client_buffer.clear()
        self.mock_outgoing_game_buffer.clear()

    def mock_send_to_client_cb(self, msg):
        self.mock_outgoing_client_buffer.append(msg)

    def mock_send_to_game_cb(self, msg):
        self.mock_outgoing_game_buffer.append(msg)

    def test_create_game(self):
        game = self.gm.create_game([b'123', b'456'])

        self.assertIn(game.GID, self.gm.games)

    def test_connect_game(self):
        game = self.gm.create_game([b'123', b'456'])
        self.gm.connect_game(game.GID)

        self.assertEqual(True, game.connected)

    def test_recv_from_client_matchmaker_create_game(self):
        to_id, from_id, msg_type, msg_content = b'1', b'0', b'0', [b'123', b'456']

        self.gm.recv_from_client(to_id, from_id, msg_type, msg_content)

        self.assertEqual(1, len(self.gm.games))

    def test_recv_from_game_forward_clients(self):
        game = self.gm.create_game([b'123', b'456'])
        msg = [b'mpwp_v1.0', b'100', b'1', game.GID, b'0', b'1', b'']
        self.gm.recv_from_game(msg)

        self.assertEqual(2, len(self.mock_outgoing_client_buffer))
        self.assertEqual(b'123', self.mock_outgoing_client_buffer[0][2])
        self.assertEqual(b'456', self.mock_outgoing_client_buffer[1][2])

    def test_forward_to_all_clients(self):
        msg = [b'mpwp_v1.0', b'100', b'1', b'0', b'0', b'1', b'']
        self.gm.forward_to_all_clients(msg, [b'123', b'456'])

        self.assertEqual(2, len(self.mock_outgoing_client_buffer))
        self.assertEqual(b'123', self.mock_outgoing_client_buffer[0][2])
        self.assertEqual(b'456', self.mock_outgoing_client_buffer[1][2])
