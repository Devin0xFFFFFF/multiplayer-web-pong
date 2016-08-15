#!/usr/bin/python

import json
import threading
from time import sleep

import zmq
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

from ..server_common import mpwp_protocol
from ..zmq.zmq_utils import zpipe
from ..game.pong_game.world import World


class GameServer(object):
    WORLD_WIDTH = 800
    WORLD_HEIGHT = 600

    ctx = None
    loop = None
    port = None
    sequence = 0
    client_input_sock = None
    client_pub_sock = None

    game = None
    GID = None

    game_thread = None
    command_enqueue = None
    command_dequeue = None

    def __init__(self, game_id=b'0', port=5556):
        self.GID = game_id
        self.port = port
        self.ctx = zmq.Context()
        self.loop = IOLoop.instance()

        self.client_input_sock = self.ctx.socket(zmq.PULL)
        self.client_pub_sock = self.ctx.socket(zmq.PUB)
        self.command_enqueue, self.command_dequeue = zpipe(self.ctx, 1000)

        self.client_input_sock.bind("tcp://*:%d" % self.port)
        self.client_pub_sock.bind("tcp://*:%d" % (self.port + 1))

        self.client_input_sock = ZMQStream(self.client_input_sock)
        self.client_input_sock.on_recv(self.handle_input)

    def start(self):
        try:
            self.game_thread = threading.Thread(target=self.game_loop, args=())
            self.game_thread.daemon = True
            self.game_thread.start()

            self.loop.start()
        except KeyboardInterrupt:
            pass

    def handle_input(self, msg):
        version, status, send_to, recv_from, data = msg
        if msg and msg[0] == self.VERSION and send_to == self.GID:
            self.command_enqueue.send_multipart([recv_from, data])

    def get_packet(self, status, send_to, msg):
        return [self.VERSION, status, send_to.encode(), self.GID, msg.encode()]

    def get_state_packet(self, state):
        formatted_state = "{0} {1} {2}".format(mpwp_protocol.GAME_STATE,
                                               self.sequence,
                                               {"state": state})
        return self.get_packet(self.STATUS_OK, "0", formatted_state)

    def publish_state(self, state):
        state_packet = self.get_state_packet(state)

        self.sequence += 1

        self.client_pub_sock.send_multipart(state_packet)

    @staticmethod
    def parse_msg_content(msg):
        # IN: b'0 11606 ["paddle1", "setPosition", [10, 10]]'
        # OUT: [0, 11606, ["paddle1", "setPosition", [10, 10]]]
        decoded_msg = msg.decode().split(" ", 2)
        decoded_msg[2] = json.loads(decoded_msg[2])

        return decoded_msg

    def get_incoming_messages(self):
        msgs = []
        has_msgs = True
        while has_msgs:
            try:
                msg = self.command_dequeue.recv_multipart(flags=zmq.NOBLOCK)
                if msg:
                    client, data = msg
                    msg_type, seq, content = self.parse_msg_content(data)
                    msg_type = int(msg_type)
                    seq = int(seq)
                    msgs.append([client, msg_type, seq, content])
            except zmq.Again:
                has_msgs = False

        return msgs

    def game_loop(self):
        self.game = World(self.WORLD_WIDTH, self.WORLD_HEIGHT)

        while True:
            cmds = self.get_incoming_messages()  # get commands from clients
            self.game.step(cmds)  # do one iteration of the pong_game
            state = self.game.get_state()  # get serialized pong_game state
            self.publish_state(state)  # publish state to clients
            sleep(self.game.game_speed / 1000)  # sleep to slow down pong_game


def main():
    server = GameServer()
    server.start()


if __name__ == "__main__":
    main()
