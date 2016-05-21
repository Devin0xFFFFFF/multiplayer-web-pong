#!/usr/bin/python

import sys
import getopt

import zmq


def main():
    #  Socket to talk to server
    context = zmq.Context()
    listener = context.socket(zmq.SUB)

    host = "localhost"
    port = "5556"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
    except getopt.GetoptError:
        print('test.py -h <host> -p <port>')
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--host"):
            host = a
        elif o in ("-p", "--port"):
            port = a
        else:
            assert False, "unhandled option"

    print(host)
    print(port)

    ip = "tcp://" + host + ":" + port

    run(listener, ip)


def run(listener, ip):
    listener.connect(ip)




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
