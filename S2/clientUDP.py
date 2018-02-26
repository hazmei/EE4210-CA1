# Author: Hazmei Bin Abdul Rahman
# Student ID: A0139920A
# AY: 17/18 Sem 2
# Module: EE4210 (Computer Communication Networks II)
# Filename: clientUDP.py
# Date: 27/02/2018

#!/usr/bin/python
import socket
import os
import sys
import signal
import logging

FILENAME = 'clientUDP.log'
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename=FILENAME,level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.info('Starting {}'.format(__file__))

req = """GET / HTTP/1.1
Host: localhost
"""


def server_handler(serverIP,serverPort):
    serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversock.settimeout(3.0)

    serversock.sendto(req,(serverIP,serverPort))
    recvbuff = serversock.recvfrom(1024) # this places the program in a blocking state

    logger.debug("Received: {}".format(recvbuff[0]))

    os._exit(0)


def main(serverIP,serverPort,numFork):
    for i in range(0,numFork):
        logger.info("Running fork {}".format(i))
        child_pid = os.fork()

        # check if child process
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

