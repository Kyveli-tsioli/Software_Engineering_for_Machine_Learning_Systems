#!/usr/bin/env python3

import argparse
import socket
import threading
import http.server
from datetime import datetime

MLLP_BUFFER_SIZE = 1024
MLLP_START_OF_BLOCK = 0x0b
MLLP_END_OF_BLOCK = 0x1c
MLLP_CARRIAGE_RETURN = 0x0d

def connect_to_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port)) # connect with host
        received = []
        while len(received) < 1:
            data = s.recv(MLLP_BUFFER_SIZE) # reads server message
            if len(data) == 0:
                raise Exception("server has no incoming messages")
            # TODO: check data validity here for if statement?
            msg = create_message("AE")
            s.sendall(msg) # send message to server
            print(f"Received {data!r}")

def create_message(msg_type):
    """
    Returns bytearray of the message to send depending on msg_type
    """
    msg = bytes(chr(MLLP_START_OF_BLOCK), "ascii")
    curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
    msg += bytes("MSH|^~\&|||||" + curr_time + "||ACK|||2.5", "ascii")
    msg += bytes(chr(MLLP_CARRIAGE_RETURN), "ascii")
    msg += bytes("MSA|" + msg_type, "ascii")
    msg += bytes(chr(MLLP_END_OF_BLOCK) + chr(MLLP_CARRIAGE_RETURN), "ascii")
    return msg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mllp", default=8440, type=int, help="Port for server")
    parser.add_argument("--pager", default=8441, type=int, help="Post on which to listen for pager requests via HTTP")
    flags = parser.parse_args()
    connect_to_server("0.0.0.0", flags.mllp)
    return

if __name__ == "__main__":
    # to kill port: lsof -i :PORT_NUM then kill PID
    main()