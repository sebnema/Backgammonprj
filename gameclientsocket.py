import socket
import random
import commands

class GameClientSocket():
    client=0
    address = ""
    port = 9898
    username = ""
    ip = ""
    lastsentclientcommand = ""
    s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

    def parseInput(self,input):
        cmd = input.split()
        if (input.lower().__contains__("pcreqplay")):
            self.lastsentclientcommand = "PCREQPLAY"
            #PCREQPLAY sebnema
            ret ='{"username": "' + self.username + '"}'
        else:
            ret="Invalid input"
        return ret

    def __init__(self, username, ip, address, port, client):
        self.client = client
        self.username = username
        self.ip = ip
        self.address = address
        self.port = port

    def clientsend(self, csocket, command, parameters):
        csocket.sendall(command + "|" + parameters)

    def run(self):
        while True:

            input = raw_input("$ ")
            if (input.lower() == "connect"):
                print("Connecting...")
                self.s.connect((self.address ,self.port))
                self.lastsentclientcommand = "PCCONN"
                parameters='{"username": "' + self.username + '", "ip": "' + self.ip + '", "serverip": "'+ self.address +'", "serverport": "' + str(self.port)+ '"}'
                self.clientsend(self.s, self.lastsentclientcommand, parameters)
            else:
                ret = self.parseInput(input)
                self.clientsend(self.s, self.lastsentclientcommand, ret)

            v = self.s.recv(1024)
            if(v != ""):
                response= commands.clientprotokolparser(self.lastsentclientcommand, v)
                print(response)
            else:
                self.s.close()



