# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest

from ...src.server_common import mpwp_protocol


class  Mpwp_Protocol_TestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Mpwp_protocol_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_mpwp_packet_(self):
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        self.assertEqual(['mpwp_v1.0', 100, 0, 0, ''], mpwp_protocol.get_mpwp_packet(mpwp_protocol.STATUS_OK, 0, 0, ""))
        
    def test_mpwp_data_packet_(self):
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        self.assertEqual(['mpwp_v1.0', 100, 0, 0, {'data':""}], mpwp_protocol.get_mpwp_data_packet(0, 0, ""))

if __name__ == '__main__':
    unittest.main()

