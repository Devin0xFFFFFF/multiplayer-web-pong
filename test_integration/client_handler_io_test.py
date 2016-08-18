import unittest

import threading
import time

from mm_server.matchmaker_server import MatchmakerServer
from client_handler.client_handler import ClientHandler
from mock_logger import MockLogger


class ClientHandlerTest(unittest.TestCase):
    logger = None
    logger_thread = None

    cli = None
    mm_server = None
    cli_thread = None
    mms_thread = None

    test_cli_id = b'ac5a49da-63f5-11e6-badf-d850e64f35c6'

    def setUp(self):
        self.msg1_unpacked = [b'mpwp_v1.0', b'100', b'0', b'1',
                              b'12345', b'0', b'{\"content\": []}']
        self.msg1_packed = '{\"data\": [\"mpwp_v1.0\", \"100\", \"0\", \"1\", ' \
                           '\"12345\", \"0\", \"{\\"content\\": []}\"]}'

        self.start_logger()
        self.start_mm_server()
        self.start_cli_handler()

        time.sleep(1)

    def tearDown(self):
            pass
        #self.mm_server.stop()
        #self.cli.stop()

    def start_logger(self):
        self.logger_thread = threading.Thread(target=self.run_logger, args=())
        self.logger_thread.daemon = True
        self.logger_thread.start()

    def run_logger(self):
        self.logger = MockLogger()
        self.logger.start()

    def start_cli_handler(self):
        self.cli_thread = threading.Thread(target=self.run_cli_handler, args=())
        self.cli_thread.daemon = True
        self.cli_thread.start()

    def start_mm_server(self):
        self.mms_thread = threading.Thread(target=self.run_mm_server, args=())
        self.mms_thread.daemon = True
        self.mms_thread.start()

    def run_mm_server(self):
        self.mm_server = MatchmakerServer()
        self.mm_server.start()

    def run_cli_handler(self):
        self.cli = ClientHandler()
        self.cli.ID = self.test_cli_id
        self.cli.connect_to_matchmaker()

    def test_chatter(self):
        msg = self.cli.get_packet(b'0', b'0', b'')
        self.cli.log(1, msg)
        self.cli.forward_to_server(msg)
        time.sleep(1)

        msg = self.logger.log_buffer[0]

        self.assertEqual(b"[b'mpwp_v1.0', b'100', b'0', b'ac5a49da-63f5-11e6-badf-d850e64f35c6', b'0', b'0']", msg)


if __name__ == '__main__':
    unittest.main()
