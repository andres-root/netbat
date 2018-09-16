import socket

target_host = 'www.google.com'
target_port = 80

# Create socket object
client = socket.socket(socket.AF_INET, socket. SOCK_STREAM)


# Connect the client
client.connect((target_host, target_port))

# Send some data
client.send(b'GET / http/1.1\r\nHost: google.com\r\n\r\n')

# Receive some darta
response = str(client.recv(4096))

print(response)
