from ..server_common.mpwp_data_sender import MPWPDataSender
from ..server_common import mpwp_protocol
from threading import Timer


class QueuedClient():
    CID = None
    accepted = False

    def __init__(self, CID):
        self.CID = CID


class MatchPool():
    accepted = 0
    loaded = False
    clients = None
    timer = None

    def __init__(self, clients):
        self.clients = clients

    def accept(self):
        self.accepted += 1

    def all_accepted(self):
        return self.accepted == len(self.clients)

    def get_client(self, CID):
        for client in self.clients:
            if (client.CID == CID):
                return client
        return None

    def create_game(self):
        pass  #


class Matchmaker(MPWPDataSender):
    queue = None
    pools = None

    socket = None
    prev_msg_num = -1

    FOUND_TIMEOUT = 5
    LOADING_TIMEOUT = 5

    def __init__(self, socket):
        self.queue = []
        self.pools = []
        self.ID = 0
        self.socket = socket
        self.socket.register_recv_callback(self.recv)

        print("{} Matchmaking Server Created @ {}".format(self.ID, self.socket.addr))

    def recv(self, msg):
        print(msg)
        if msg and msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_OK:
            data = mpwp_protocol.msg_data(msg)
            self.handle_incoming(msg[mpwp_protocol.MSG_FROM], data)

    def send(self, id, msg):
        return self.socket.send(id, msg)

    def handle_incoming(self, id, data):
        cmd_type = data[1]
        if cmd_type == mpwp_protocol.MATCHMAKER_QUEUE:
            print("{} : ENQUEUE".format(id))
            self.enqueue(id)
        elif cmd_type == mpwp_protocol.MATCHMAKER_DEQUEUE:
            print("{} : DEQUEUE".format(id))
            self.dequeue(id)
        elif cmd_type == mpwp_protocol.MATCHMAKER_ACCEPT:
            print("{} : ACCEPT".format(id))
            self.accept(id)
        elif cmd_type == mpwp_protocol.MATCHMAKER_DECLINE:
            print("{} : DECLINE".format(id))
            self.decline(id)
        else:
            print("{} : ???".format(id))

    def enqueue(self, CID):
        if not self.client_queued(CID):
            self.queue.append(QueuedClient(CID))
            self.matchmake()

    def client_queued(self, CID):
        return len([x for x in self.queue if x.CID == CID]) == 1

    def dequeue(self, CID):
        self.queue = [x for x in self.queue if x.CID != CID]

    def accept(self, CID):
        pool, client = self.get_pool_and_client(CID)
        pool.accepted += 1
        client.accepted = True
        if (pool.all_accepted()):
            pool.timer.cancel()
            self.pools.remove(pool)
            self.create_game(pool)

    def create_game(self, pool):
        self.alert_match_loading(pool.clients)
        pool.timer = Timer(self.LOADING_TIMEOUT, self.loading_timeout, [pool])
        pool.timer.start()

        pool.loaded = True  # need to add code above thisso timeout may happen first
        pool.timer.cancel()

        self.alert_match_launch(pool.clients)

        print("MATCHMAKING SERVER GAME CREATED WITH: {}".format(pool.clients))
        # probably want to multithread this, as it could take a while

    def decline(self, CID):
        pool, client = self.get_pool_and_client(CID)
        for c in pool.clients:
            if c != client:
                c.accepted = False
                self.alert_match_decline(c.CID)
                self.queue.append(c)
        self.pools.remove(pool)

    def found_timeout(self, pool):
        if pool not in self.pools:
            return  # exit if match already accepted / declined

        for client in pool.clients:
            if client.accepted:
                client.accepted = False
                self.queue.append(client)
        self.pools.remove(pool)
        print("MATCHMAKING SERVER MATCH TIMEOUT")

    def loading_timeout(self, pool):
        if pool.loaded:
            return
        for client in pool.clients:
            self.queue.append(client)
        print("MATCHMAKING SERVER LOADING TIMEOUT")

    def get_pool_and_client(self, CID):
        for pool in self.pools:
            client = pool.get_client(CID)
            if (client):
                return (pool, client)
        return (None, None)

    def matchmake(self):
        if (len(self.queue) > 1):
            clients = [self.queue[0], self.queue[1]]
            self.queue = self.queue[2:]
            self.create_pool(clients)

    def create_pool(self, clients):
        pool = MatchPool(clients)
        self.pools.append(pool)
        self.alert_match_found(clients)
        pool.timer = Timer(self.FOUND_TIMEOUT, self.found_timeout, [pool])
        pool.timer.start()

    def alert_match_found(self, clients):
        for client in clients:
            msg = self.get_packet(client.CID, mpwp_protocol.MATCHMAKER_FOUND, "")
            self.send(client.CID, msg)

    def alert_match_loading(self, clients):
        for client in clients:
            msg = self.get_packet(client.CID, mpwp_protocol.MATCHMAKER_LOADING, "")
            self.send(client.CID, msg)

    def alert_match_launch(self, clients):
        for client in clients:
            msg = self.get_packet(client.CID, mpwp_protocol.MATCHMAKER_LAUNCH, "")
            self.send(client.CID, msg)

    def alert_match_decline(self, CID):
        msg = self.get_packet(CID, mpwp_protocol.MATCHMAKER_DECLINE, "")
        self.send(CID, msg)
