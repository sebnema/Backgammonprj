import socket
import commands
import  backgammon
import sys

from threading import Thread

s = socket.socket()
host = socket.gethostname()
#print(host)
port = 9898
#tumple degistirelemez liste
s.bind((host,port))

# 30 tane conn que ya atip bekletebiliyor
s.listen(30)

global lastsentservercomand
lastsentservercomand = ""

class ClientThread(Thread):
    def __init__(self, clientSocket,clientAddr):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr

    def run(self):
        while 1:
            try:
                # It will hang here, even if I do close on the socket
                data = self.clientSocket.recv(2048)
                print "Got data: ", data
                response = commands.serverprotocolparser(self.clientSocket, data)
                commands.serversend(self.clientSocket, lastsentservercomand, response)
            except Exception, err:
                sys.stderr.write('ERROR: %s\n' % str(err))
                break

        self.clientSocket.close()

while True:
    # baglanti kurulduktan sonra atanan connection degiskenleri iki tane donuyor
    clientSocket, clientaddr = s.accept()
    print 'Got a new connection from: ', clientaddr

    clientThread = ClientThread(clientSocket,clientaddr)
    clientThread.start()

