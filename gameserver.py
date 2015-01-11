import gameserversocket

class server:
    conn=0
    #users=[]
    socket=0

    def __init__(self,address,port,connections):
        # Point Of No Return!!!
        self.socket = gameserversocket.GameServerSocket(address, port, connections, self)

if __name__ == "__main__":
    gamesocketServer = server("127.0.0.1", 9898, 30)


