import time
import random
import Queue
import json
import user
from pprint import pprint

class Object:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def fromjson(val):
    #E.g. val is {"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}
    data = json.loads(val)
    return data

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
            #response = '{"message": "'+valobj['message']+'", "opponent": "'+valobj['opponent']+'", "gameid": "'+valobj['gameid']+'"}'
            response = 'Your opponent is ' + valobj['opponent'] + '.You are ready to start playing.'
        if (retcommand == "SRVERR"):
            response = valobj['message']
    else:
        response = "Something went wrong on server"

    return response

def processcommand(csocket, manager, data):
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
        response = pcconn(csocket, manager, username, ip, serverip, serverport)
    elif (command == "PCREQPLAY"):
        #parsing PCREQPLAY {"username": "Joe", "ip": "11.11.11.11"}
        username = valobj['username']
        response = pcreqplay(csocket, manager, username)
    elif (command == "PCQPLAY"):
        #parsing PCPLAY {"username": "Joe", "matchid": "saasdasd"}
        username = valobj['username']
        matchid = valobj['matchid']
        response = pcplay(csocket, manager, username, matchid)
    else:
        response = "ERR"
    return response



def pcconn(csocket, manager, username, ip, serverip, serverport):
    print("PCCONN command received")

    ifuserexists = manager.checkifUserExists(username)
    if (ifuserexists):
        response = 'SRVERR|{"message": "Username ' + username + ' already exists. Choose another name"}'
        return response
    else:
        isadded = manager.addToUsers(csocket,username,ip,-1)

    if(isadded):
        player = manager.findUserByName(username)
        player.state = "Connected"
        response = 'SRVOK|{"message": "Hi ' + username+ ', You are connected to ' + serverip + ', ' + serverport+ '. Make your choice. 1)I want to play: pcreqplay 2)I want to watch: pcreqwath"}'
    else:
        response = 'SRVERR|{"message": "Something went wrong..."}'
    return response

def pcreqplay(csocket, manager, username):
    print("PCREQPLAY command received")
    match, opponent = manager.getActiveMatchandOpponentOfPlayer(username)

    if(match):
        response = 'SRVOK|{"message": "You are playing a match", "opponent": "'+str(opponent.username)+'", "matchid": "'+str(match.id)+'" }'
    else:
        matchid = -1
        #get player user object from all users list
        player = manager.findUserByName(username)

        #get opponent user object from queue
        opponentusername = manager.getOpponentFromWaitingList()

        # if opponent not exists, player added to waiting list
        if (opponentusername==0):
            if(player<>0):
                #player added to waiting list
                isadded = manager.addToWaitingList(username)
                if (isadded):
                    response = 'SRVERR|{"message": "No active user to play. You are added to waiting list. Wait or make another choice"}'
                else:
                    response = 'SRVERR|{"message": "Player could not add to waiting list"}'
        else:
            opponent = manager.findUserByName(opponentusername)
            #if opponent exists a new match created for player and the opponent
            matchid = manager.createNewMatch(player,opponent)

            #after new match created, set activegameid of each player and oppponent user data
            if (matchid >0):
                if isinstance(player,user.User):
                    player.activematchid = matchid
                    player.state = "Waiting"
                if isinstance(opponent,user.User):
                    opponent.activematchid = matchid
                    opponent.state = "Waiting"
                response = 'SRVOK|{"message": "Successful", "opponent": "'+str(opponentusername)+'", "gameid": "'+str(matchid)+'" }'
    return response

def pcplay(manager,username, matchid):
    print("PCPLAY command received")
    gameid, board= manager.getInitialGameBoard(matchid)
    if(gameid>0):
        response = board
    return response

def pcthrowdice(manager, username, gameid):
    print("PCTHROWDICE command sent")
    dice_1 = random.randrange(1,6)
    dice_2 = random.randrange(1,6)
    dice = dice_1 +""+ dice_2
    response = response = 'SRVOK|{"message": "Successful", "dice": "'+str(dice)+'", "gameid": "'+str(gameid)+'" }'

def pcsendmove(username, ip, gameid, move):
    print("PCSENDMOVE command received")

def pcwrongmovealert(username, ip, gameid):
    print("PCWRONGMOVEALERT command received")


def pcreqwatch(username, ip, gameid):
    print("PCREQWATCH command received")

def pcwatch(username, ip, gameid):
    print("PCWATCH command received")

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
