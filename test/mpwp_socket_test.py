# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest

import mpwp_socket

class  Mpwp_socket_TestCase(unittest.TestCase):
    def setUp(self):
        self.nw = mpwp_socket.MockNetwork()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_network_bind(self):
        s = mpwp_socket.MockRouterSocket(self.nw)
        s.bind("0.0.0.0:8000")
        
        self.assertEqual(['0.0.0.0:8000'], list(self.nw.endpoints.keys()))
        
    def test_network_connect(self):
        s = mpwp_socket.MockRouterSocket(self.nw)
        s.bind("0.0.0.0:8000")
        s2 = mpwp_socket.MockDealerSocket(self.nw)
        s2.connect("0.0.0.0:8000")
        
        self.assertEqual(s2.endpoint, s)

if __name__ == '__main__':
    unittest.main()

