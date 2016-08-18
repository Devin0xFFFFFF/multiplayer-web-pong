import unittest

from server_common.mpwp_data_sender import MPWPDataSender


class ClientHandlerTest(unittest.TestCase):
    content1 = [b'cid1', b'cid2']
    content1_packed = b''

    def setUp(self):
        self.mds = MPWPDataSender(log_level=0)

    def tearDown(self):
        pass

    def test_assign_id(self):
        self.assertIsNone(self.mds.ID)
        self.mds.assign_id()
        self.assertIsNotNone(self.mds.ID)

    def test_get_packet(self):
        packet = self.mds.get_packet(b'0', b'0')
        self.assertEqual([b'mpwp_v1.0', b'100', b'0', None, b'0', b'0'], packet)


if __name__ == '__main__':
    unittest.main()
