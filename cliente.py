

import socket

sock = socket.socket()
host = socket.gethostname()
port = 12345

sock.connect((host, port))
sock.send("Hola servidor!")

f = open('mensaje_a_enviar.txt', 'rb')

print('Enviando...')

l = f.read(1024)

while (l):
    print('Enviando...')
    sock.send(l)
    l = f.read(1024)
f.close()

print('Enviado')
print(sock.recv(1024))

sock.close()
