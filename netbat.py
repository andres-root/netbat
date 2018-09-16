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


def cliend_sender(buffer):

    # Set a TCP object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the target host
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:

            # Wait for data back
            recv_len = 1
            response = ''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print(response)

            # Wait for more input
            buffer = raw_input('')
            buffer += '\n'

            # Send it off
            client.send(buffer)
    except Exception as err:
        print('[*] Exception! Exiting.')
        print(srt(err))

        # Close connection
        client.close()


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

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif 0 in ('-l', '--listen'):
            LISTEN = True
        elif o in ('-c', '--commandshell'):
            COMMAND = True
        elif o in ('-u', '--upload'):
            UPLOAD_DESTINATION = a
        elif o in ('-t', '--target'):
            TARGET = a
        elif o in ('-p', '--port'):
            PORT = int(a)
        else:
            assert False, 'Unhandled option'

    # Listen or just send data from stdin
    if not LISTEN and len(TARGET) and PORT > 0:

        # Read the buffer from the commandline
        # This will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # Send data off
        client_sender(buffer)

    if LISTEN:
        server_loop()





















