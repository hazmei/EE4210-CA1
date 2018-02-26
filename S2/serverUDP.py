# Author: Hazmei Bin Abdul Rahman
# Student ID: A0139920A
# AY: 17/18 Sem 2
# Module: EE4210 (Computer Communication Networks II)
# Filename: serverUDP.py
# Date: 27/02/2018

#!/usr/bin/python
import socket
import re
import os
import time
import sys
import signal
import logging

FILENAME = 'serverUDP.log'
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename=FILENAME,level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
logger.info('Starting {}'.format(__file__))

try:
    # create global socket object
    serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except Exception as e:
    logger.critical("Unable to create socket: {}".format(e))


def client_handler(recvbuff,serversock):
    data = recvbuff[0]
    addr = recvbuff[1]

    logger.info("Got connection from {}".format(addr))

    logger.debug("Data received: {}".format(data))

    # check received data and response accordingly
    if "GET / HTTP/1.1" in data: # received data does not contain input
        logger.debug("received request for default html")
        serversock.sendto(build_response(),addr)
        logger.debug("Response sent!")
    else: # unknown data structure received
        logger.info("Received unknown data structure from {}".format(addr))

    os._exit(0)


def main(port):
    try:
        # bind to all interfaces
        serversock.bind(('0.0.0.0',port))
        logger.info("Binding to port {}".format(port))
    except Exception as e:
        logger.critical("Error on bind: {}".format(e))
        sys.exit(1)

    while True:
        try:
            # put the program in a blocking state until receive something
            recvbuff = serversock.recvfrom(1024)
            data = recvbuff[0]

            if not data:
                break

            # fork process to handle client
            child_pid = os.fork()

            #check if child process
            if child_pid==0:
                print("Connection with client successful")
                client_handler(recvbuff,serversock)
            else:
                os.waitpid(-1, os.WNOHANG)
        except Exception as e:
            logger.critical("Error on communication: {}".format(e))


def build_response():
    responseOKstr = 'HTTP/1.1 200 OK\r\n' +\
      time.strftime('Date: %a, %d %b %Y %H:%M:%S SGT\r\n') +\
      'Server: Apache/1.3.41 (Unix) mod_perl/1.31\r\n' +\
      'Content-Type: text/html\r\n' + '\r\n' +\
      '<HTML><HEAD>\r\n' +\
      '<TITLE>200 OK</TITLE>' +\
      '</HEAD><BODY>\r\n' +\
      'EE-4210: Continuous assessment\r\n' +\
      '</BODY></HTML>\r\n'

    return responseOKstr


# function to exit the program gracefully and close the socket before terminating
def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    try:
        if raw_input("\nReally quit? (y/n): ").lower().startswith('y'):
            logger.info('Exiting {}'.format(__file__))
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info('Exiting {}'.format(__file__))
        sys.exit(1)

    signal.signal(signal.SIGINT, exit_gracefully)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        serverPort = int(sys.argv[1])
    else:
        print("Invalid command!")
        print("Command: python {} <port>".format(__file__))
        logger.critical("Invalid number of args. Terminating now.")
        sys.exit(1)

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    print("To exit: ctrl+c")
    print("Note: Output are logged at {}".format(FILENAME))

    main(serverPort)
