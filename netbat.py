import sys
import socket
import getopt
import threading
import subprocess


LISTEN = False
PORT = 0
EXECUTE = ''
COMMAND = False
UPLOAD_DESTINATION = ''
TARGET = ''
UPLOAD = False


# TODO: Implement this function
def usage():
    print('Need a target.')
    pass


def main():
    global LISTEN
    global PORT
    global EXECUTE
    global COMMAND
    global UPLOAD_DESTINATION
    global TARGET

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle:t:p:cu', ['help', 'listen', 'execute', 'target', 'port', 'upload'])
    except Exception as err:
        print(str(err))
        usage()
