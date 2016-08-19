from client_handler.client_handler import ClientHandler


class MockClientHandler(ClientHandler):
    to_client = []
    to_server = []
    from_client = []
    from_server = []

    def __init__(self):
        super(ClientHandler, self).__init__(log_level=0)

    def send_ws(self, msg):
        self.from_server.append(msg)

    def recv_ws(self):
        while not self.to_server:
            pass
        return self.to_server.pop(0)

    def send_server(self, msg):
        self.from_client.append(msg)

    def recv_server(self):
        while not self.to_client:
            pass
        return self.to_client.pop(0)

    def mock_client_send(self, msg):
        self.to_server.append(msg)

    def mock_server_send(self, msg):
        self.to_client.append(msg)

    def clear(self):
        self.to_client.clear()
        self.to_server.clear()
        self.from_client.clear()
        self.from_server.clear()
