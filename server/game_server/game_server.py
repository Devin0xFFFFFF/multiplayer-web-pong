#!/usr/bin/python

import threading
from time import sleep

import zmq


def main():
    #  Socket to talk to server
    context = zmq.Context()
    inputs = context.socket(zmq.PULL)
    clients = context.socket(zmq.PUB)

    host = "*"
    in_port = "5556"
    out_port = "5557"

    cli_to = "tcp://" + host + ":" + out_port
    cli_from = "tcp://*:" + in_port

    inputs.bind(cli_from)  # bind for client inputs
    clients.bind(cli_to)  # bind for client publishing

    # thread = threading.Thread(target=listen_client, args=(server,))
    # thread.start()

    poller = zmq.Poller()
    poller.register(inputs, zmq.POLLIN)  # poll for player input

    i = 0

    while True:
        msg = "{\"HEAD\": \"CMD\", \"BODY\": {\"targetID\":\"ball\", \"action\": \"move\", \"args\": [10]}}"
        #print(str(i) + ": " + msg)
        i += 1
        clients.send_string(msg)

        sockets = dict(poller.poll(0))

        if inputs in sockets:
            in_msg = inputs.recv_string()
            clients.send_string(in_msg)
            #print(in_msg)

        sleep(0.015)

    inputs.close()
    clients.close()

if __name__ == "__main__":
    main()
