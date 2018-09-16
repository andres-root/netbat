import socket

target_host = '127.0.0.1'
target_port = 9999

# Create socket object
client = socket.socket(socket.AF_INET, socket. SOCK_STREAM)


# Connect the client
client.connect((target_host, target_port))

# Send some data
client.send(b'Hello friend.')

# Receive some darta
response = str(client.recv(4096))

print(response)
