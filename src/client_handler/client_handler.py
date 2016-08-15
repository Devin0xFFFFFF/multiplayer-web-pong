#!/usr/bin/python
import json
import sys
import getopt
import threading

import time
import zmq

VERSION = b'mpwp0.1'


def pack_data(data):
    decoded = [x.decode() for x in data]
    return json.dumps({"data": decoded})


def unpack_data(data):
    print(data)
    loaded = json.loads(data)["data"]
    return [x.encode() for x in loaded]


def listen_client(server):
    while True:
        data = server.recv_multipart()
        if data:
            if data[0] == VERSION:
                print(unpack_data(pack_data(data)))
                send(pack_data(data))
            else:
                pass  # send VERSION_MISMATCH_ERROR


def send_server(server, data):
    unpacked = unpack_data(data)
    server.send_multipart(unpacked)  # forward stdin to gm_server


def send(msg):
    print(msg)
    sys.stdout.flush()


def recv(msg):
    return sys.stdin.readline()


def main():
    #  Socket to talk to gm_server
    context = zmq.Context()
    server = context.socket(zmq.DEALER)

    server_host = "localhost"
    server_to_port = "5556"
    server_from_port = "5557"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:i:o:", ["gm_server=", "inport=", "outport="])
    except getopt.GetoptError:
        print('test.py -s <gm_server> -i <inport> -o <outport>')
        sys.exit(2)

    for o, a in opts:
        if o in ("-s", "--gm_server"):
            server_host = a
        elif o in ("-i", "--inport"):
            server_to_port = a
        elif o in ("-o", "--outport"):
            server_from_port = a
        else:
            assert False, "unhandled option"

    server_send = "tcp://" + server_host + ":" + server_to_port
    server_recv = "tcp://" + server_host + ":" + server_from_port

    server.connect(server_send)  # connect to pong_game gm_server

    print("Connected.")

    thread = threading.Thread(target=listen_client, args=(listener,))
    thread.daemon = True
    thread.start()

    print("Listening...")

    while True:
        # data = recv()
        data = '{"data": ["mpwp0.1", "100", "0", "0", "0 11606 [\\"paddle1\\", \\"set_position\\", [10, 10]]"]}'
        send_server(server, data)
        time.sleep(1)

    server.close()
    listener.close()

if __name__ == "__main__":
    main()
