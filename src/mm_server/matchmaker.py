from threading import Thread, Timer

from server_common.mpwp_data_sender import MPWPDataSender
from server_common import mpwp_protocol


class MMClient(object):
    CID = None
    accepted = False

    def __init__(self, CID):
        self.CID = CID


class MatchPool(object):
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
            if client.CID == CID:
                return client
        return None

    def create_game(self):
        pass  #


class Matchmaker(MPWPDataSender):
    queue = None
    pools = None
    clients = None

    send_cb = None
    create_game_cb = None

    FOUND_TIMEOUT = 5
    LOADING_TIMEOUT = 5

    def __init__(self, send_cb, create_game_cb):
        self.queue = []
        self.pools = []
        self.clients = {}
        self.ID = mpwp_protocol.MATCHMAKER_ID
        self.send_cb = send_cb
        self.create_game_cb = create_game_cb

    def reset(self):
        self.queue.clear()
        self.pools.clear()
        self.clients.clear()

    def recv(self, sender_id, msg_type, msg_content):
        if msg_type == mpwp_protocol.MATCHMAKER_QUEUE:
            self.log(1, "{} : ENQUEUE".format(sender_id))
            self.enqueue(sender_id)
        elif msg_type == mpwp_protocol.MATCHMAKER_DEQUEUE:
            self.log(1, "{} : DEQUEUE".format(sender_id))
            self.dequeue(sender_id)
        elif msg_type == mpwp_protocol.MATCHMAKER_ACCEPT:
            self.log(1, "{} : ACCEPT".format(sender_id))
            self.accept(sender_id)
        elif msg_type == mpwp_protocol.MATCHMAKER_DECLINE:
            self.log(1, "{} : DECLINE".format(sender_id))
            self.decline(sender_id)
        else:
            self.log(1, "{} : ???".format(sender_id))

    def send(self, msg):
        self.send_cb(msg)

    def enqueue(self, CID):
        if not self.client_queued(CID):
            self.queue.append(MMClient(CID))
            self.matchmake()

    def client_queued(self, CID):
        return len([x for x in self.queue if x.CID == CID]) == 1

    def dequeue(self, CID):
        self.queue = [x for x in self.queue if x.CID != CID]

    def accept(self, CID):
        pool, client = self.get_pool_and_client(CID)
        pool.accepted += 1
        client.accepted = True
        if pool.all_accepted():
            pool.timer.cancel()
            self.pools.remove(pool)
            self.create_game(pool)

    def create_game(self, pool):
        self.alert_match_loading(pool.clients)
        pool.timer = Timer(self.LOADING_TIMEOUT, self.loading_timeout, [pool])
        pool.timer.start()

        create_game_msg = self.get_packet(mpwp_protocol.GAME_MANAGER_ID,
                                          mpwp_protocol.GAME_CREATE,
                                          pool.clients)
        self.create_game_cb(create_game_msg)

        pool.loaded = True
        pool.timer.cancel()

        self.alert_match_launch(pool.clients)

        self.log(1, "MATCHMAKING SERVER GAME CREATED WITH: {}".format(pool.clients))
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
        self.log(1, "MATCHMAKING SERVER MATCH TIMEOUT")

    def loading_timeout(self, pool):
        if pool.loaded:
            return
        for client in pool.clients:
            self.queue.append(client)
        self.log(1, "MATCHMAKING SERVER LOADING TIMEOUT")

    def get_pool_and_client(self, CID):
        for pool in self.pools:
            client = pool.get_client(CID)
            if client:
                return pool, client
        return None, None

    def matchmake(self):
        if len(self.queue) > 1:
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
            self.send(msg)

    def alert_match_loading(self, clients):
        for client in clients:
            msg = self.get_packet(client.CID, mpwp_protocol.MATCHMAKER_LOADING, "")
            self.send(msg)

    def alert_match_launch(self, clients):
        for client in clients:
            msg = self.get_packet(client.CID, mpwp_protocol.MATCHMAKER_LAUNCH, "")
            self.send(msg)

    def alert_match_decline(self, CID):
        msg = self.get_packet(CID, mpwp_protocol.MATCHMAKER_DECLINE, "")
        self.send(msg)
