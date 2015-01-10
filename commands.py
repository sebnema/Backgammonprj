import time
import random
import backgammon
import Queue
import json
from pprint import pprint

global lastsentservercomand

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def fromjson(val):
    #E.g. val is {"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}
    data = json.loads(val)
    return data

def clientsend(csocket, command, parameters):
    csocket.sendall(command + "|" + parameters)

def serversend(ssocket, lastsentservercomand, message):
    lastsentservercomand = message.split("|")[0]
    ssocket.sendall(message)

def clientprotokolparser(sentcommand, data):
    #SRVOK|{"message": "Hi sebnema, You are connected to 11.11.11.11, 9898"}
    msg = data.split("|")
    if(len(msg)>0):
        retcommand = msg[0]
    if(len(msg)>1):
        parameters = msg[1]
        valobj = fromjson(parameters)

    if (sentcommand == "PCCONN"):
        if (retcommand == "SRVOK"):
            response = valobj['message']
        if (retcommand == "SRVERR"):
            response = valobj['message']
    elif (sentcommand == "PCREQPLAY"):
        if (retcommand == "SRVOK"):
           response = valobj['message']
        if (retcommand == "SRVERR"):
            response = valobj['message']
    else:
        response = "Something went wrong on server"

    return response

def serverprotocolparser(csocket, data):
    #get command and parameters(If exists)
    input = data.split("|")
    if(len(input)>0):
        command = input[0]
    if(len(input)>1):
        val = input[1]
        valobj = fromjson(val)

    if (command == "PCCONN"):
        #parsing PCCONN|{"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}
        username = valobj['username']
        ip = valobj['ip']
        serverip = valobj['serverip']
        serverport = valobj['serverport']
        response = pcconn(csocket,username, ip, serverip, serverport)
    elif (command == "PCREQPLAY"):
        #parsing PCREQPLAY {"username": "Joe", "ip": "11.11.11.11"}
        username = valobj['username']
        ip = valobj['ip']
        response = pcreqplay(csocket,username, ip)
    else:
        response = "ERR"
    return response

def pcconn(csocket, username, ip, serverip, serverport):
    print("PCCONN command received")

    manager = backgammon.GameManager()
    ifuserexists = manager.checkifUserExists(username)
    if (ifuserexists):
        response = 'SRVERR|{"message": "Username ' + username + ' already exists. Choose another name"}'
        return response

    isadded = manager.addToWaitingList(username,ip)
    if(isadded):
         response = 'SRVOK|{"message": "Hi ' + username+ ', You are connected to ' + serverip + ', ' + serverport+ '"}'
    else:
        response = 'SRVERR|{"message": "Something went wrong..."}'
    return response


def pcreqplay(csocket, username, ip):
    print("PCREQPLAY command received")


def pcplay(username, ip, gameid):
    print("PCPLAY command received")

def pcreqwatch(username, ip, gameid):
    print("PCREQWATCH command received")

def pcwatch(username, ip, gameid):
    print("PCWATCH command received")

def pcthrowdice(username, ip):
    print("PCTHROWDICE command sent")
    dice_1 = random.randrange(1,6)
    dice_2 = random.randrange(1,6)
    dice = dice_1 +""+ dice_2

def pcsendmove(username, ip, gameid, move):
    print("PCSENDMOVE command received")


def pcwrongmovealert(username, ip, gameid):
    print("PCWRONGMOVEALERT command received")


def pcbearoff(username, ip, gameid, move):
    print("PCBEAROFF command received")

def pcbearoff(username, ip, gameid, move):
    print("PCBEAROFF command received")

def pcend(username, ip):
    print("PCEND command received")

def srvhbeat(username, opponent):
    print("SRVHBEAT  command received")

def srvackdice(gameid,player,dice):
    print("SRVACKDICE command sent")

def srvackmove(gameid,player,playerip,gameboard):
    print("SRVACKMOVE command sent")

def srvackwrongmove(username,ip,gameid,previousgameboard):
    print("SRVACKWRONGMOVE command sent")
