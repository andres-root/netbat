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


def client_sender(buffer):

    # Set a TCP object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the target host
        client.connect((TARGET, PORT))

        if len(buffer):
            client.send(buffer)

        while True:

            # Wait for data back
            recv_len = 1
            response = ''

            while recv_len:
                data = client.recv(4096).decode()
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
        print('[*] {}'.format(str(err)))

        # Close connection
        client.close()
        print('Connection closed.')


def client_handler(client_socket):
    global UPLOAD
    global EXECUTE
    global COMMAND

    # Check for upload
    if len(UPLOAD_DESTINATION):

        # Read all in all of the bytes and write to the destination
        file_buffer = ''

        # Keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # Now take these bytes and try to write them out
        try:
            file_descriptor = open(UPLOAD_DESTINATION, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # Acknowledge that the file was written
            client_socket.send('Successfully saved file to {0}\r\n'.format(
                UPLOAD_DESTINATION))
        except Exception:
            client_socket.send('Failed to save file to {0}\r\n'.format(
                UPLOAD_DESTINATION))

    # Check for command execution
    if len(EXECUTE):

        # Run the command
        output = run_command(EXECUTE)

        client_socket.send(output)

    # Go into another loop if a command shell was requested
    if COMMAND:
        while True:

            # Show a simple prompt
            client_socket.send(b'<netbat:#> ')

            # Receive untill a linefeed (enter key) is seen
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += str(client_socket.recv(1024))

            # Send back the command output
            response = run_command(cmd_buffer)

            # Send back the response
            client_socket.send(response)


def server_loop():
    global TARGET

    # If no target is defined, we listen on all interfaces
    if not len(TARGET):
        TARGET = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TARGET, PORT))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Spin off a thread to handle the new client
        client_thread = threading.Thread(
            target=client_handler, args=(client_socket,))

        client_thread.start()


def run_command(command):

    # Trim the newline
    command = command.rstrip()

    # Run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except Exception:
        output = 'Failed to execute command. \r\n'

    # Send the output back to the lient
    return output


def usage(error=None):
    print('NetBat Network Tool')
    print('\r\n')
    print('Usage: netbat.py -t target_host -p port')
    print('-l --listen              - listen on [host]:[port] for incoming connections')
    print('-e --execute=file_to_run - execute the given file upon receiving a connection')
    print('-c --command             - initialize a command shell')
    print('-u --upload=destination  - upon receiving a connection upload a file and write to [destination]')
    print('\r\n')
    print('\r\n')
    print('Examples: ')
    print('netbat.py -t 192.168.0.1 -p 5555 -l -c')
    print('netbat.py -t 192.168.0.1 -p 5555 -l -u=C:\\target.exe')
    print('netbat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"')
    print('echo \'ABCDEFGHI\' | ./netbat.py -t 192.168.11.12 -p 135')

    if error:
        print('Errors: {0}'.format(error))

    sys.exit(0)


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
        usage(err)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
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


main()
