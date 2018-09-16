import socket

target_host = '127.0.0.1'
target_port = 8000

try:

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send some data
    client.sendto(b'asdfasdfa', (target_host, target_port))

    # Receive some data
    data, addr = str(client.recvfrom(4096))

    print(data)

except socket.timeout:
    print('Cannot connect to {0} on port {1}'.format(target_host, target_port))
