import socket
s = socket.socket()
host = socket.gethostname()
port = 9898

s.connect((host,port))
while True:
    v = s.recv(1024)
    if(v != ""):
        print(v)
    else:
        s.close()
