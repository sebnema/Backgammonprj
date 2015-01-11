import socket
import gameclientsocket
from sys import version_info

class client:

    def __init__(self, username, ip, address,port):
        # Point Of No Return!!!
        self.socket = gameclientsocket.GameClientSocket(username, ip, address, port, self)
        self.socket.run()

if __name__ == "__main__":
    #Screen 1: Connect to Server
    username = raw_input("Please enter username: ")
    serverip = raw_input("Please enter server ip: ")
    serverport = raw_input("Please enter server port: ")
    #TODO ip ve port sorunu
    ip = socket.gethostname()
    serverip  = "127.0.0.1"
    port = 9898 #int(serverport)
    serverport = port
    # end of Screen 1

    gamesocketClient= client(username, ip,serverip, serverport)


