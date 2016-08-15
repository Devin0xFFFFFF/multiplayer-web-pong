# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from ...src.mm_server.mm_client import MMClient
from ...src.mm_server.matchmaker import Matchmaker
from .mpwp_socket import MockNetwork, MockDealerSocket, MockRouterSocket

__author__ = "Devin"
__date__ = "$Aug 6, 2016 5:26:49 PM$"

MM_ADDR = "0.0.0.0:8000"

class MPWebPongMain():
    nw = None
    mm_sock = None
    cli1_sock = None
    cli2_sock = None
    mm = None
    cli1 = None
    cli2 = None
    
    def __init__(self):
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
        
        self.cli1.connect(MM_ADDR)
        self.cli2.connect(MM_ADDR)
        
        # cmd_line_interface.run(self.mm, self.cli1, self.cli2)
        
        # self.cli1.queue()
        # self.cli2.queue()
        
        # self.cli1.accept()
        # self.cli2.decline()

if __name__ == "__main__":
    mpwp = MPWebPongMain()

