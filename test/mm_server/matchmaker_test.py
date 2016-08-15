# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest

import matchmaker
import mpwp_socket

class  Matchmaker_TestCase(unittest.TestCase):
    mm_addr = "0.0.0.0:8000"
    
    def setUp(self):
        self.nw = mpwp_socket.MockNetwork()
        self.mms = mpwp_socket.MockRouterSocket(self.nw)
        self.mms.bind(self.mm_addr)
        self.connect_clients()
        self.mm = matchmaker.Matchmaker(self.mms)

    def connect_clients(self):
        self.c1 = mpwp_socket.MockDealerSocket(self.nw)
        self.c1.connect(self.mm_addr)
        
        self.c2 = mpwp_socket.MockDealerSocket(self.nw)
        self.c2.connect(self.mm_addr)
    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_matchmaker_queue(self):
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        self.mm.enqueue(12345)
        self.assertEqual(1, len(self.mm.queue))
        
        id = self.mm.queue[0].CID
        self.assertEqual(12345, id)
        
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
        pool = self.create_match([1,2])
        
        self.mm.accept(1)
        
        self.assertEqual(1, pool.accepted)
        self.assertEqual(True, pool.clients[0].accepted)
        
    def test_matchmaker_decline(self):
        pool = self.create_match([1,2])
        self.mm.decline(1)
        
        self.assertEqual(0, len(self.mm.pools))
        
    def test_matchmaker_decline_with_accept(self):
        pool = self.create_match([1,2])
        self.mm.accept(2)
        self.assertEqual(True, pool.clients[1].accepted)
        self.mm.decline(1)
        
        self.assertEqual(0, len(self.mm.pools))
        self.assertEqual(False, pool.clients[1].accepted)
        self.assertEqual(1, len(self.mm.queue))
        
    def test_matchmaker_timeout(self):
        pool = self.create_match([1,2])
        self.mm.timeout(pool)
        
        self.assertEqual(0, len(self.mm.pools))
        self.assertEqual(0, len(self.mm.queue))
        
    def test_matchmaker_all_accept(self):
        pool = self.create_match([1,2])
        self.mm.accept(1)
        self.mm.accept(2)
        
        self.assertEqual(0, len(self.mm.pools))
        
    def test_matchmaker_found_packet(self):
        self.assertEqual(['mpwp_v1.0', 100, 1, 0, {'data': [0, 2, '']}], self.mm.get_found_message(1))
        
    def create_match(self, ids):
        for id in ids:
            self.mm.enqueue(id)
        
        return self.mm.pools[0]

if __name__ == '__main__':
    unittest.main()

