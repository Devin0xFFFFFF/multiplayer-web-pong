#!/usr/bin/python

import sys
import getopt
import threading

import zmq


def listen_client(server):
    while True:
        data = server.recv_string()
        send(data)


def send(msg):
    print(msg)
    sys.stdout.flush()


def recv():
    return sys.stdin.readline()


def main():
    #  Socket to talk to server
    context = zmq.Context()
    server = context.socket(zmq.PUSH)
    listener = context.socket(zmq.SUB)

    server_host = "localhost"
    server_to_port = "5556"
    server_from_port = "5557"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:i:o:", ["server=", "inport=", "outport="])
    except getopt.GetoptError:
        print('test.py -s <server> -i <inport> -o <outport>')
        sys.exit(2)

    for o, a in opts:
        if o in ("-s", "--server"):
            server_host = a
        elif o in ("-i", "--inport"):
            server_to_port = a
        elif o in ("-o", "--outport"):
            server_from_port = a
        else:
            assert False, "unhandled option"

    server_send = "tcp://" + server_host + ":" + server_to_port
    server_recv = "tcp://" + server_host + ":" + server_from_port

    server.connect(server_send)  # connect to game server
    listener.connect(server_recv)  # subscribe to game server
    listener.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Connected.")

    thread = threading.Thread(target=listen_client, args=(listener,))
    thread.daemon = True
    thread.start()

    print("Listening...")

    while True:
        data = recv()
        server.send_string(data)  # forward stdin to server
        #server.send_string(data)

    server.close()
    listener.close()

# string = socket.recv_string()
#
# while True:
#     msg = "{\"HEAD\": \"CMD\", \"BODY\": {\"targetID\":\"ball\", \"action\": \"move\", \"args\": [10]}}"
#     print(msg)
#     stdout.flush()
#     data = stdin.readline()
#     print(data)
#     stdout.flush()
#     sleep(0.015)

if __name__ == "__main__":
    main()
