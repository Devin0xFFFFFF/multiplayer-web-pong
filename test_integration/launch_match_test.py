# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest

from ..src.mm_server.mock_mm_client import MMClient

from ..src.mm_server.matchmaker import Matchmaker
from ..test.mm_server.mpwp_socket import MockNetwork, MockDealerSocket, MockRouterSocket


class Launch_match_TestCase(unittest.TestCase):
    MM_ADDR = "0.0.0.0:8000"

    def setUp(self):
        self.nw = MockNetwork()
        self.mm_sock = MockRouterSocket(self.nw)
        self.cli1_sock = MockDealerSocket(self.nw)
        self.cli2_sock = MockDealerSocket(self.nw)

        self.mm_sock.bind("0.0.0.0:8000")
        self.cli1_sock.bind("192.168.1.1:8000")
        self.cli2_sock.bind("192.168.1.2:8000")

        self.mm = Matchmaker(self.mm_sock)
        self.cli1 = MMClient(self.cli1_sock)
        self.cli2 = MMClient(self.cli2_sock)

        self.cli1.connect(self.MM_ADDR)
        self.cli2.connect(self.MM_ADDR)

    # def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_launch_match_(self):
        self.cli1.queue()
        self.cli2.queue()

        self.cli1.accept()
        self.cli2.accept()

        self.assertEqual(0, len(self.mm.queue))
        self.assertEqual(0, len(self.mm.pools))

    def test_decline_match(self):
        self.cli1.queue()
        self.cli2.queue()

        self.cli1.accept()
        self.cli2.decline()

        self.assertEqual(1, len(self.mm.queue))
        self.assertEqual(MMClient.state_queuing, self.cli1.state)
        self.assertEqual(MMClient.state_waiting, self.cli2.state)

    def test_loading_timeout(self):
        self.cli1.queue()
        self.cli2.queue()

        pool = self.mm.pools[0]
        self.mm.found_timeout(pool)
        pool.timer.cancel()
        self.cli1.found_timer.cancel()
        self.cli2.found_timer.cancel()

        self.assertEqual(0, len(self.mm.queue))


if __name__ == '__main__':
    unittest.main()
