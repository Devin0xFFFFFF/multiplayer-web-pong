# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest

from server_common import mpwp_protocol


class  Mpwp_Protocol_TestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = Mpwp_protocol_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_get_uuid(self):
        ID = mpwp_protocol.get_uuid()
        self.assertEqual(bytes, type(ID))
        self.assertEqual(36, len(ID))

    def test_get_mpwp_packet(self):
        packet = mpwp_protocol.get_mpwp_packet(mpwp_protocol.STATUS_OK, b'0', b'0', b'12345', b'0')
        self.assertEqual([b'mpwp_v1.0', b'100', b'0', b'0', b'12345', b'0'], packet)
        
    def test_get_mpwp_status_packet(self):
        packet = mpwp_protocol.get_mpwp_status_packet(b'100', b'0', b'1')
        self.assertEqual([b'mpwp_v1.0', b'100', b'0', b'1'], packet)

    def test_get_mpwp_content_packet(self):
        packet = mpwp_protocol.get_mpwp_content_packet(b'0', b'1', b'12', b'0')
        self.assertEqual([b'mpwp_v1.0', b'100', b'0', b'1', b'12', b'0'], packet)

    def test_get_log_packet(self):
        packet = mpwp_protocol.get_log_packet(b'0', b'241', b'1', b'Critical Error!')
        self.assertEqual([b'mpwp_v1.0', b'300', b'3', b'0', b'241', b'1', b'Critical Error!'], packet)

    def test_get_msg_content(self):
        msg = [b'mpwp_v1.0', b'100', b'0', b'0', b'12345', b'0', b'', b'', b'']
        self.assertEqual([b'', b'', b''], mpwp_protocol.msg_content(msg))

if __name__ == '__main__':
    unittest.main()

