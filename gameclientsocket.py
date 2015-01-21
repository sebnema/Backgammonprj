import socket
import random
import commands
import signal
import sys,select
from threading import Timer
from multiprocessing import Process

TIMEOUT = 10 # number of seconds your want for timeout

class GameClientSocket():
    client=0
    address = ""
    port = 9898
    username = ""
    ip = ""
    lastsentclientcommand = ""
    s = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

    def __init__(self, username, ip, address, port, client):
        self.client = client
        self.username = username
        self.ip = ip
        self.address = address
        self.port = port
        #signal.signal(signal.SIGTERM, self.interrupted)

    def reconnect(self):
        toBreak = False
        while True:
            self.s.close()
            try:
                self.s.connect((self.address ,self.port))
                toBreak = True
            except:
                print ("except")
            if toBreak:
                break


    def parseInput(self,input):
        cmd = input.split()
        if (input.lower().__contains__("pcconn")):
            #PCCONN sebnema
            print("Connecting...")

            try:
               self.s.connect((self.address ,self.port))
            except socket.error, e:
                #if e.errno == errno.ECONNRESET:
                # Handle disconnection -- close & reopen socket etc.
                self.reconnect()
                #else:
                    # Other error, re-raise
                 #   raise

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
            #PCSENDMOVE 123123123 12 4/2 4/3
            gameid = cmd[1]
            dice = cmd[2]
            move1 = cmd[3]
            move2 = cmd[4]
            ret ='{"username": "' + self.username + '", "gameid": "'+ str(gameid)+'", "dice":"' + str(dice) + '", "move":"' + str(move1) + ' ' + str(move2) +'"  }'
        else:
            ret = "Invalid command"
        return ret



    def clientsend(self, csocket, command, parameters):
        csocket.sendall(command + "||" + parameters)

    def receivemessage(self):
        v = self.s.recv(1024)
        if(v != ""):
            response= commands.clientprotokolparser(self.lastsentclientcommand, v)
            print(response)
        else:
            self.s.close()

    def run(self):
        while True:
            input =  raw_input("$ ")
            if (len(input)>0):
                ret = self.parseInput(input)
                self.clientsend(self.s, self.lastsentclientcommand, ret)

            self.receivemessage()




