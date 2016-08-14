from mpwp_data_sender import MPWPDataSender
import mpwp_protocol
from threading import Timer

class Client(MPWPDataSender):
    state = None
    socket = None
    MATCHMAKER_ID = 0
    
    state_waiting = 0
    state_queuing = 1
    state_found = 2
    state_loading = 3
    state_launching = 4
    state_playing = 5
    
    FOUND_TIMEOUT = 5
    LOADING_TIMEOUT = 5
    
    found_timer = None
    loading_timer = None
    
    def __init__(self, socket):
        self.assign_id()
        self.state = 0
        self.socket = socket
        self.socket.register_recv_callback(self.recv)
        print("{} Client Created @ {}".format(self.ID, self.socket.addr))
        
    def get_state(self):
        return self.state
    
    def connect(self, mm_addr):
        self.socket.connect(mm_addr, alias=self.ID)
    
    def recv(self, msg):
        print(msg)
        if msg and msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_OK:
            data = mpwp_protocol.msg_data(msg)
            self.handle_incoming(msg[mpwp_protocol.MSG_FROM], data)
        
    def send(self, msg):
        self.socket.send(msg)
        
    def handle_incoming(self, id, data):
        if id == 0: #MATCHMAKER_ID
            msg_type = data[1]
            if msg_type == mpwp_protocol.MATCHMAKER_FOUND and self.state == self.state_queuing:
                print("{} CLIENT MATCH FOUND".format(self.ID))
                self.found_timer = Timer(self.FOUND_TIMEOUT, self.found_timeout)
                self.found_timer.start()
                self.state = self.state_found
            elif msg_type == mpwp_protocol.MATCHMAKER_DECLINE and self.state == self.state_found:
                self.state = self.state_queuing
            elif msg_type == mpwp_protocol.MATCHMAKER_LOADING and self.state == self.state_found:
                print("{} CLIENT MATCH LOADING".format(self.ID))
                self.found_timer.cancel()
                self.loading_timer = Timer(self.LOADING_TIMEOUT, self.loading_timeout)
                self.loading_timer.start()
                self.state = self.state_loading
            elif msg_type == mpwp_protocol.MATCHMAKER_LAUNCH and self.state == self.state_loading:
                print("{} CLIENT MATCH LAUNCH".format(self.ID))
                self.loading_timer.cancel()
                self.state = self.state_launching
    
    def found_timeout(self):
        if not self.state == self.state_found:
            return # exit if match already loaded / declined
        self.state = self.state_waiting
        print("{} CLIENT MATCH TIMEOUT".format(self.ID))
        
    def loading_timeout(self):
        if not self.state == self.state_loading:
            return # exit if match already loaded / declined
        self.state = self.state_queuing
        print("{} CLIENT LOADING TIMEOUT".format(self.ID))
            
    def get_matchmaker_packet(self, cmd):
        return self.get_packet(self.MATCHMAKER_ID, cmd, "")
        
    def queue(self):
        self.state = self.state_queuing
        self.send(self.get_matchmaker_packet(mpwp_protocol.MATCHMAKER_QUEUE))
        
    def dequeue(self):
        self.state = self.state_waiting
        self.send(self.get_matchmaker_packet(mpwp_protocol.MATCHMAKER_DEQUEUE))
        
    def accept(self):
        self.send(self.get_matchmaker_packet(mpwp_protocol.MATCHMAKER_ACCEPT))
        
    def decline(self):
        self.state = self.state_waiting
        self.send(self.get_matchmaker_packet(mpwp_protocol.MATCHMAKER_DECLINE))