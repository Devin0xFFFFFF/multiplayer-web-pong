import unittest
import threading
import time
import queue

from gm_server import game_manager_server
from mm_server import matchmaker_server
from client_handler import client_handler


class MockStdin(object):
    inputs = None

    def __init__(self):
        self.inputs = queue.Queue()

    def write(self, msg):
        self.inputs.put(msg)

    def readline(self):
        while self.inputs.empty():
            pass
        return self.inputs.get()


class ConnectToGame_AcceptanceTest(unittest.TestCase):
    gms = None
    mms = None
    cli1 = None
    cli2 = None

    def launch_game_manager(self):
        self.gm_thread = threading.Thread(target=self.run_game_manager)
        self.gm_thread.setDaemon(True)
        self.gm_thread.start()

    def launch_matchmaker(self):
        self.mm_thread = threading.Thread(target=self.run_matchmaker)
        self.mm_thread.setDaemon(True)
        self.mm_thread.start()

    def launch_client_handlers(self):
        self.ch_thread1 = threading.Thread(target=self.run_client_handler1)
        self.ch_thread1.setDaemon(True)
        self.ch_thread1.start()
        self.ch_thread2 = threading.Thread(target=self.run_client_handler2)
        self.ch_thread2.setDaemon(True)
        self.ch_thread2.start()

    def run_game_manager(self):
        self.gms = game_manager_server.GameManagerServer()
        self.gms.start()

    def run_matchmaker(self):
        self.mms = matchmaker_server.MatchmakerServer()
        self.mms.start()

    def run_client_handler1(self):
        self.cli1 = client_handler.ClientHandler()
        self.cli1.stdin = MockStdin()
        self.cli1.start()

    def run_client_handler2(self):
        self.cli2 = client_handler.ClientHandler()
        self.cli2.stdin = MockStdin()
        self.cli2.start()

    def input(self, cli, msg):
        time.sleep(0.5)
        cli.stdin.write(msg)
        time.sleep(0.5)

    def setUp(self):
        self.launch_game_manager()
        self.launch_matchmaker()
        self.launch_client_handlers()
        time.sleep(1)

    def tearDown(self):
        pass

    def test_connect_to_game(self):
        # TEST CONNECT TO CLIENT HANDLER
        self.input(self.cli1, '{\"data\": [\"mpwp_v1.0\", \"200\", \"2\", \"\"]}')

        self.assertIsNot(b'', self.cli1.ID)

        cid1 = self.cli1.ID.decode()

        # TEST CONNECT TO MATCHMAKER SERVER
        self.input(self.cli1, '{\"data\": [\"mpwp_v1.0\", \"200\", \"0\", \"' + cid1 + '\"]}')

        self.assertEqual(True, self.cli1.connected)

        # TEST ENQUEUE FOR MATCH
        self.input(self.cli1, '{\"data\": [\"mpwp_v1.0\", \"100\", \"0\", \"' + cid1 + '\", \"0\", \"0\"]}')

        self.assertEqual(1, len(self.mms.matchmaker.queue))
        self.assertEqual(cid1, self.mms.matchmaker.queue[0].CID.decode())

        # TEST CONNECT AND ENQUEUE SECOND CLIENT

        self.input(self.cli2, '{\"data\": [\"mpwp_v1.0\", \"200\", \"2\", \"\"]}')

        cid2 = self.cli2.ID.decode()

        self.input(self.cli2, '{\"data\": [\"mpwp_v1.0\", \"200\", \"0\", \"' + cid2 + '\"]}')
        self.input(self.cli2, '{\"data\": [\"mpwp_v1.0\", \"100\", \"0\", \"' + cid2 + '\", \"0\", \"0\"]}')

        self.assertEqual(0, len(self.mms.matchmaker.queue))
        self.assertEqual(1, len(self.mms.matchmaker.pools))

        # TEST BOTH CLIENTS ACCEPT MATCH

        self.input(self.cli1, '{\"data\": [\"mpwp_v1.0\", \"100\", \"0\", \"' + cid1 + '\", \"0\", \"3\"]}')
        self.input(self.cli2, '{\"data\": [\"mpwp_v1.0\", \"100\", \"0\", \"' + cid2 + '\", \"0\", \"3\"]}')

        self.assertEqual(0, len(self.mms.matchmaker.pools))

        time.sleep(1)

        self.assertEqual(1, len(self.gms.manager.games))
