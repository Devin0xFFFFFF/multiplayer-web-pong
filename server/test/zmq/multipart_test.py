import threading

import time
import zmq


def send(ctx):
    pub = ctx.socket(zmq.PUB)
    pub.bind("inproc://testmp")
    while True:
        pub.send_multipart([b'frame0', b'frame1'])
        time.sleep(0.1)


def main():
    ctx = zmq.Context()

    send_thread = threading.Thread(target=send, args=(ctx,))
    send_thread.daemon = True
    send_thread.start()

    sub = ctx.socket(zmq.SUB)
    sub.connect("inproc://testmp")
    sub.setsockopt(zmq.SUBSCRIBE, b'')
    while True:
        msg = sub.recv_multipart()
        print(msg)


if __name__ == '__main__':
    main()
