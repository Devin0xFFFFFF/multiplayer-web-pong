class MPWPSocket():
    addr = None
    recv_callback = None
    
    def __init__(self):
        pass
    
    def register_recv_callback(self, recv_callback):
        self.recv_callback = recv_callback
    
    def bind(self, addr):
        self.addr = addr
        
    def connect(self, addr):
        pass
    
    def send(self, msg):
        pass
        
    def recv(self, msg):
        if(self.recv_callback):
            self.recv_callback(msg)
        else:
            raise

class MockNetwork():
    endpoints = None
    
    def __init__(self):
        self.endpoints = {}
        
    def bind(self, socket):
        self.endpoints[socket.addr] = socket
        
    def connect(self, addr):
        return self.endpoints.get(addr)

class MockDealerSocket(MPWPSocket):
    network = None
    endpoint = None
    
    def __init__(self, network):
        self.network = network
        
    def bind(self, addr):
        super(MockDealerSocket, self).bind(addr)
        self.network.bind(self)
        
    def connect(self, addr, alias=None):
        if not alias:
            alias = addr
        self.endpoint = self.network.connect(addr)
        self.endpoint.connect(alias, self)
        
    def send(self, msg):
        if self.endpoint:
            self.endpoint.recv(msg)
        else:
            print("Endpoint Does Not Exist!")
    
class MockRouterSocket(MPWPSocket):
    network = None
    connections = None
    
    def __init__(self, network):
        self.network = network
        self.connections = {}
        
    def bind(self, addr):
        super(MockRouterSocket, self).bind(addr)
        self.network.bind(self)
        
    def connect(self, alias, endpoint):
        self.connections[alias] = endpoint
        
    def send(self, alias, msg):
        endpoint = self.connections.get(alias)
        if endpoint:
            endpoint.recv(msg)
        else:
            print("Endpoint Does Not Exist!")
    
class MockPipe(MPWPSocket):
    def send(self, msg):
        self.recv(msg) #Send to recv end of the pipe 