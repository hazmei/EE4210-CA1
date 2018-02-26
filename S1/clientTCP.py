# Author: Hazmei Bin Abdul Rahman
# Student ID: A0139920A
# AY: 17/18 Sem 2
# Module: EE4210 (Computer Communication Networks II)
# Filename: clientTCP.py
# Date: 27/02/2018

#!/usr/bin/python
import socket
import os
import sys
import signal
import logging
from socket import SHUT_RDWR

FILENAME = 'clientTCP.log'
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename=FILENAME,level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.info('Starting {}'.format(__file__))

req = """GET / HTTP/1.1
Host: localhost
"""


def server_handler(host,port):
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serversock.connect((host, port))
    except Exception as e:
        logger.critical("Error on connection: {}".format(e))

    serversock.send(req)

    logger.debug("Received: {}".format(serversock.recv(1024)))
    logger.info("Terminating connection to {}".format(host))
    serversock.shutdown(SHUT_RDWR)
    serversock.close()

    os._exit(0)


def main(serverIP,serverPort,numFork):
    for i in range(0,numFork):
        logger.info("Running fork {}".format(i))
        child_pid = os.fork()

        if child_pid==0:
            server_handler(serverIP,serverPort)
        else:
            os.waitpid(-1, os.WNOHANG)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        serverIP = sys.argv[1]
        serverPort = int(sys.argv[2])
        numFork = int(sys.argv[3])
    else:
        print("Invalid command!")
        print("Command: python {} <server-ip> <server-port> <num-fork>".format(__file__))
        logger.critical("Invalid number of args. Terminating now.")
        sys.exit(1)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    print("To exit: ctrl+c")
    print("Note: Output are logged at {}".format(FILENAME))

    main(serverIP,serverPort,numFork)

    logger.info("Terminating {}".format(__file__))
    sys.exit(0)
