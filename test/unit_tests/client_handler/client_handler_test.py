import unittest

from mock_client_handler import MockClientHandler


class ClientHandlerTest(unittest.TestCase):
    mock_cli_id = b'ac5a49da-63f5-11e6-badf-d850e64f35c6'
    msg1_unpacked = [b'mpwp_v1.0', b'100', b'ac5a49da-63f5-11e6-badf-d850e64f35c6',
                          b'1', b'12345', b'0', b'{\"content\": []}']
    msg1_packed = '{\"data\": [\"mpwp_v1.0\", \"100\", \"ac5a49da-63f5-11e6-badf-d850e64f35c6\", \"1\", ' \
                       '\"12345\", \"0\", \"{\\"content\\": []}\"]}'

    msg2_unpacked = [b'mpwp_v1.0', b'100', b'1',
                          b'ac5a49da-63f5-11e6-badf-d850e64f35c6', b'12345', b'0', b'{\"content\": []}']

    msg2_packed = '{\"data\": [\"mpwp_v1.0\", \"100\", \"1\", \"ac5a49da-63f5-11e6-badf-d850e64f35c6\", ' \
                       '\"12345\", \"0\", \"{\\"content\\": []}\"]}'

    connect_msg_incoming = [b'mpwp_v1.0', b'200', b'2', b'', b'', b'', b'']

    connect_msg_outgoing = '{\"data\": [\"mpwp_v1.0\", \"201\", \"ac5a49da-63f5-11e6-badf-d850e64f35c6\", \"2\"]}'

    def setUp(self):
        self.cli_h = MockClientHandler()
        self.cli_h.ID = self.mock_cli_id

    def tearDown(self):
        self.cli_h.clear()

    def test_pack(self):
        packed = self.cli_h.pack(self.msg1_unpacked)
        self.assertEqual(self.msg1_packed, packed)

    def test_unpack(self):
        unpacked = self.cli_h.unpack(self.msg1_packed)
        self.assertEqual(self.msg1_unpacked, unpacked)

    def test_client_handler_listen_server(self):
        self.cli_h.mock_server_send(self.msg1_unpacked)
        self.cli_h.mock_server_send(None)
        self.cli_h.connected = True
        self.cli_h.listen_server()

        self.assertEqual(1, len(self.cli_h.from_server))
        self.assertEqual(self.cli_h.from_server[0], self.msg1_packed)

    def test_client_handler_listen_client(self):
        self.cli_h.mock_client_send(self.msg2_packed)
        self.cli_h.mock_client_send(None)
        self.cli_h.connected = True
        self.cli_h.listen_client()

        self.assertEqual(1, len(self.cli_h.from_client))
        self.assertEqual(self.cli_h.from_client[0], self.msg2_unpacked)

    def test_forward_to_server(self):
        self.cli_h.forward_to_server(self.msg2_unpacked)

        self.assertEqual(1, len(self.cli_h.from_client))
        self.assertEqual(self.cli_h.from_client[0], self.msg2_unpacked)

    def test_handle_connection(self):
        self.cli_h.ID = None

        self.assertEqual(None, self.cli_h.ID)

        self.cli_h.handle_connection(self.connect_msg_incoming)

        self.assertIsNotNone(self.cli_h.ID)

        self.assertEqual(1, len(self.cli_h.from_server))

    def test_send_connect_ok(self):
        self.cli_h.send_connect_ok(b'2')

        self.assertEqual(1, len(self.cli_h.from_server))
        self.assertEqual(self.cli_h.from_server[0], self.connect_msg_outgoing)

    def test_connect_to_game_manager_after_matchmaker(self):
        self.cli_h.connect_to_matchmaker()
        self.cli_h.disconnect()
        self.cli_h.connect_to_game_manager()

        self.assertEqual(True, self.cli_h.connected)

if __name__ == '__main__':
    unittest.main()
