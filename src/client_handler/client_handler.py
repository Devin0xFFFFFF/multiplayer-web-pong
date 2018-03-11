#!/usr/bin/python
import json
import sys
import threading

import time
import zmq

from server_common import mpwp_protocol

from server_common import config

from server_common.mpwp_data_sender import MPWPDataSender


class ClientHandler(MPWPDataSender):
    connected = False
    server_sock = None
    stdin = sys.stdin

    def __init__(self):
        #  Socket to talk to servers
        super(ClientHandler, self).__init__()
        self.ID = b''
        self.log(1, "Client Handler Started")

    def start(self):
        # start thread to listen to client
        thread = threading.Thread(target=self.listen_client, args=())
        thread.daemon = True
        thread.start()

        # need to add some AUTH stuff to get UUID
        # AUTH must check if UUID already exists somewhere due to disconnect
        self.listen_server()

        self.log(1, "Shutting Down.")

    def connect_to_matchmaker(self):
        self.connect_to_server(mpwp_protocol.MATCHMAKER_ID, config.MATCHMAKER_ADDR)

    def connect_to_game_manager(self):
        self.connect_to_server(mpwp_protocol.GAME_MANAGER_ID, config.GAME_MANAGER_ADDR)

    def connect_to_server(self, server_id, server_addr):
        self.log(1, "Connecting...")
        self.reset_socket()
        self.server_sock.connect(server_addr)
        self.connected = True
        self.log(1, "Connected to: {}".format(server_addr))

        self.send_connect_ok(server_id)

    def reset_socket(self):
        self.disconnect()

        try:
            self.log(1, "Creating Socket...")
            self.server_sock = self.context.socket(zmq.DEALER)
        except Exception as err:
            self.log(1, "{}".format(err))

        self.server_sock.setsockopt(zmq.IDENTITY, self.ID)

    def disconnect(self):
        # add some error checking here if socket fails to close
        if self.connected and self.server_sock:
            self.log(1, "Disconnecting")
            self.connected = False
            self.server_sock.close()
            self.server_sock = None

    @staticmethod
    def pack(msg):
        decoded = [x.decode() for x in msg]

        return json.dumps({"data": decoded})

    @staticmethod
    def unpack(msg):
        loaded = json.loads(msg)["data"]
        return [x.encode() for x in loaded]

    def listen_server(self):
        while True:
            if self.connected:
                try:
                    msg = self.recv_server()
                except zmq.Again:
                    msg = b'1'
                except Exception as err:
                    self.log(1, "Error: {}".format(err))
                if msg:
                    if type(msg) == list:
                        self.log(1, msg)
                        if msg[mpwp_protocol.MSG_VERSION] == mpwp_protocol.VERSION:
                            if msg[mpwp_protocol.MSG_TO] == self.ID:
                                self.send_ws(self.pack(msg))
                            else:
                                pass  # send INCORRECT_TO_ID_ERROR to server
                        else:
                            pass  # send VERSION_MISMATCH_ERROR
                    else:
                        pass  # no msg available
                else:
                    self.log(1, "Fatal Error")
                    break  # fatal error
            else:
                pass  # what to do when not connected?

    def listen_client(self):
        while True:
            msg = self.recv_ws()
            try:
                msg = self.unpack(msg)
            except TypeError:
                msg = None
            self.log(1, msg)
            if msg:
                if msg[mpwp_protocol.MSG_VERSION] == mpwp_protocol.VERSION:
                    if self.ID:
                        if not self.connected:
                            if msg[mpwp_protocol.MSG_TO] == mpwp_protocol.MATCHMAKER_ID:
                                self.connect_to_matchmaker()
                            elif msg[mpwp_protocol.MSG_TO] == mpwp_protocol.GAME_MANAGER_ID:
                                self.connect_to_game_manager()
                        else:
                            if msg[mpwp_protocol.MSG_TO] == mpwp_protocol.CLIENT_HANDLER_ID:
                                self.handle_client_msg(msg)
                            else:
                                self.forward_to_server(msg)
                    else:
                        self.handle_connection(msg)
                else:
                    pass  # send VERSION_MISMATCH_ERROR
            else:
                break  # fatal error

    def forward_to_server(self, msg):
        if msg[mpwp_protocol.MSG_FROM] == self.ID:
            self.send_server(msg)
        else:
            pass  # send INCORRECT_FROM_ID_ERROR to client

    def handle_connection(self, msg):
        if msg[mpwp_protocol.MSG_TO] == mpwp_protocol.CLIENT_HANDLER_ID:
            if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_CONNECT:
                if msg[mpwp_protocol.MSG_FROM] != b'':  # need to check if it exists somewhere
                    # self.check_existing_id()
                    pass  # eventually check GAME_MANAGER to see if received ID exists
                    # could possibly rejoin game after losing connection
                else:
                    self.assign_id()
                    self.send_connect_ok(mpwp_protocol.CLIENT_HANDLER_ID)
        else:
            pass  # send INCORRECT_TO_ID_ERROR to client

    def handle_client_msg(self, msg):
        if msg[mpwp_protocol.MSG_STATUS] == mpwp_protocol.STATUS_DISCONNECT:
            self.disconnect()

    def send_ws(self, msg):
        print(msg)
        sys.stdout.flush()

    def recv_ws(self):
        return self.stdin.readline()

    def send_server(self, msg):
        self.server_sock.send_multipart(msg)

    def recv_server(self):
        return self.server_sock.recv_multipart(flags=zmq.NOBLOCK)

    def send_connect_ok(self, FROM):
        msg = mpwp_protocol.get_mpwp_status_packet(mpwp_protocol.STATUS_CONNECT_OK,
                                                   self.ID,
                                                   FROM)
        msg = self.pack(msg)
        self.log(1, msg)
        self.send_ws(msg)


def main():
    ch = ClientHandler()
    ch.start()


if __name__ == "__main__":
    main()
