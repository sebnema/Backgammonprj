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
        if (input.lower().__contains__("pcconn")):
            #PCCONN sebnema
            print("Connecting...")
            self.s.connect((self.address ,self.port))
            self.lastsentclientcommand = "PCCONN"
            ret='{"username": "' + self.username + '", "ip": "' + self.ip + '", "serverip": "'+ self.address +'", "serverport": "' + str(self.port)+ '"}'
        elif (input.lower().__contains__("pcreqplay")):
            self.lastsentclientcommand = "PCREQPLAY"
            #PCREQPLAY sebnema
            ret ='{"username": "' + self.username + '"}'
        elif (input.lower().__contains__("pcplay")):
            self.lastsentclientcommand = "PCPLAY"
            #PCPLAY 12123123234
            matchid = cmd[1]
            ret ='{"username": "' + self.username + '", "matchid": "'+ str(matchid) +'"}'
        elif (input.lower().__contains__("pcthrowdice")):
            self.lastsentclientcommand = "PCTHROWDICE"
            #PCTHROWDICE 123123123
            gameid = cmd[1]
            ret ='{"username": "' + self.username + '", "gameid": "'+ str(gameid)+'"}'
        elif (input.lower().__contains__("pcsendmove")):
            self.lastsentclientcommand = "PCSENDMOVE"
            #PCTHROWDICE 123123123 12:4/2 4/3
            gameid = cmd[1]
            move = cmd[2]
            ret ='{"username": "' + self.username + '", "gameid": "'+ str(gameid)+'", "move":"' + str(move) + '" }'
        else:
            ret = "Invalid command"
        return ret

    def __init__(self, username, ip, address, port, client):
        self.client = client
        self.username = username
        self.ip = ip
        self.address = address
        self.port = port

    def clientsend(self, csocket, command, parameters):
        csocket.sendall(command + "||" + parameters)

    def run(self):
        while True:

            input = raw_input("$ ")

            ret = self.parseInput(input)
            self.clientsend(self.s, self.lastsentclientcommand, ret)

            v = self.s.recv(1024)
            if(v != ""):
                response= commands.clientprotokolparser(self.lastsentclientcommand, v)
                print(response)
            else:
                self.s.close()



