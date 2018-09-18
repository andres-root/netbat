import socket

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))

f = open('torecv.png', 'wb')

s.listen(5)

while True:
    c, addr = s.accept()
    print('Conectandose a', addr)
    print("Recibiendo...")
    l = c.recv(1024)
    while (l):
        print "Receiving..."
        f.write(l)
        l = c.recv(1024)
    f.close()
    print('Listo')
    c.send('Recibido')
    c.close()
