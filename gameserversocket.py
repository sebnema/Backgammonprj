import socket
import gamesocketthread
import user
import random
import gamemanager

class GameServerSocket():
    manager = gamemanager.GameManager()
    server=0

    def __init__(self, address, port, connections, server):
        self.server = server
        server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        server.bind ( ( address, port ) )
        server.listen ( connections )
        while True:
            channel, details = server.accept()

            gamesocketthread.GameSocketThread (channel, details, self.manager).start()


