# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest

from mm_server import matchmaker


class Matchmaker_TestCase(unittest.TestCase):

    mock_outgoing_buffer = []

    def setUp(self):
        self.mm = matchmaker.Matchmaker(self.mock_send_cb)

    def tearDown(self):
        self.mm = None
        self.mock_outgoing_buffer.clear()

    def mock_send_cb(self, msg):
        self.mock_outgoing_buffer.append(msg)

    def test_recv(self):
        pass

    def test_enqueue(self):
        self.mm.enqueue(b'12345')
        self.assertEqual(1, len(self.mm.queue))

        id = self.mm.queue[0].CID
        self.assertEqual(b'12345', id)

    def test_matchmaker_queue_duplicate(self):
        self.mm.enqueue(12345)
        self.mm.enqueue(12345)

        self.assertEqual(1, len(self.mm.queue))

    def test_matchmaker_dequeue(self):
        self.mm.enqueue(1)

        self.mm.dequeue(1)
        self.assertEqual(0, len(self.mm.queue))

    def test_matchmaker_matchmake(self):
        self.mm.enqueue(1)
        self.mm.enqueue(2)

        self.assertEqual(0, len(self.mm.queue))
        self.assertEqual(1, len(self.mm.pools))

        pool = self.mm.pools[0]
        c = pool.clients[0].CID
        self.assertEqual(1, c)

    def test_matchmaker_accept(self):
        pool = self.create_match([1, 2])

        self.mm.accept(1)

        self.assertEqual(1, pool.accepted)
        self.assertEqual(True, pool.clients[0].accepted)

    def test_matchmaker_decline(self):
        pool = self.create_match([1, 2])
        self.mm.decline(1)

        self.assertEqual(0, len(self.mm.pools))

    def test_matchmaker_decline_with_accept(self):
        pool = self.create_match([1, 2])
        self.mm.accept(2)
        self.assertEqual(True, pool.clients[1].accepted)
        self.mm.decline(1)

        self.assertEqual(0, len(self.mm.pools))
        self.assertEqual(False, pool.clients[1].accepted)
        self.assertEqual(1, len(self.mm.queue))

    def test_matchmaker_found_timeout(self):
        pool = self.create_match([1, 2])
        self.mm.found_timeout(pool)

        self.assertEqual(0, len(self.mm.pools))
        self.assertEqual(0, len(self.mm.queue))

    def test_matchmaker_all_accept(self):
        pool = self.create_match([1, 2])
        self.mm.accept(1)
        self.mm.accept(2)

        self.assertEqual(0, len(self.mm.pools))

    def create_match(self, ids):
        for id in ids:
            self.mm.enqueue(id)

        pool = self.mm.pools[0]
        pool.timer.cancel()

        return pool


if __name__ == '__main__':
    unittest.main()
