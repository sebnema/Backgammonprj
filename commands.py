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
    val=str(val).replace("\n","Char103")
    data = json.loads(val)
    #for d in data:
    #    str(d).replace("Char103","\n")
    return data

def clientprotokolparser(sentcommand, data):
    #SRVOK|{"message": "Hi sebnema, You are connected to 11.11.11.11, 9898"}
    msg = data.split("||")
    if(len(msg)>0):
        retcommand = msg[0]
    if(len(msg)>1):
        parameters = msg[1]
        valobj = fromjson(parameters)
    response = ""
    if (sentcommand == "PCCONN"):
        if (retcommand == "SRVOK"):
            response = valobj['message']
        elif (retcommand == "SRVERR"):
            response = valobj['message']
    elif (sentcommand == "PCREQPLAY"):
        if (retcommand == "SRVOK"):
            response = 'Your opponent is ' + valobj['opponent'] + '.You are ready to start playing. pcplay ' + str(valobj['matchid']) + ''
        elif (retcommand == "SRVERR"):
            response = valobj['message']
    elif (sentcommand == "PCPLAY"):
        if (retcommand == "SRVOK"):
            response = valobj['board'] +"\n" + "You can start throw dice -> pcthrowdice " + valobj["gameid"]
        elif (retcommand == "SRVERR"):
            response = valobj['message']
    elif (sentcommand == "PCTHROWDICE"):
        if (retcommand == "SRVOK"):
            response = 'Dice is ' + valobj['dice'] + ". Send move -> pcsendmove " +valobj["gameid"]+ " " + valobj['dice'] + ": move1 move2"
        elif (retcommand == "SRVERR"):
            response = valobj['message']
    elif (sentcommand == "PCSENDMOVE"):
        if (retcommand == "SRVOK"):
            response = valobj['board'] +"\n" + "You can send wrong move alert -> pcwrongmovealert " + valobj["gameid"]
        elif (retcommand == "SRVERR"):
            response = valobj['message']
    else:
        response = "Something went wrong on server"

    response=str(response).replace("Char103","\n")
    return response

def processcommand(csocket, manager, data):
    #get command and parameters(If exists)
    users=[]
    val=""
    command=""
    input = data.split("||")
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
    elif (command == "PCPLAY"):
        #parsing PCPLAY {"username": "Joe", "matchid": "123123"}
        username = valobj['username']
        matchid = valobj['matchid']
        response = pcplay(csocket, manager, username, matchid)
    elif (command == "PCTHROWDICE"):
        #parsing PCTHROWDICE {"username": "Joe", "gameid": "123123"}
        username = valobj['username']
        gameid = valobj['gameid']
        response = pcthrowdice(csocket, manager, username, gameid)
        users = srvackusers(csocket, manager, username, gameid, response)
    elif (command == "PCSENDMOVE"):
        #parsing PCSENDMOVE {"username": "Joe", "gameid": "123123", "move": "12: 4/3 3/1"}
        username = valobj['username']
        gameid = valobj['gameid']
        dice= valobj['dice']
        move = valobj['move']
        response = pcsendmove(csocket, manager, username, gameid, dice, move)
        users = srvackusers(csocket, manager, username, gameid, response)
    else:
        response = "ERR"
    return response, users

def pcconn(csocket, manager, username, ip, serverip, serverport):
    print("PCCONN command received")

    ifuserexists = manager.checkifUserExists(username)
    if (ifuserexists):
        response = 'SRVERR||{"message": "Username ' + username + ' already exists. Choose another name"}'
        return response
    else:
        isadded = manager.addToUsers(csocket,username,ip,-1)

    if(isadded):
        player = manager.findUserByName(username)
        player.state = "Connected"
        response = 'SRVOK||{"message": "Hi ' + username+ ', You are connected to ' + serverip + ', ' + serverport+ '. Make your choice. 1)I want to play: pcreqplay 2)I want to watch: pcreqwatch"}'
    else:
        response = 'SRVERR||{"message": "Something went wrong..."}'
    return response

def pcreqplay(csocket, manager, username):
    print("PCREQPLAY command received")
    match, opponent = manager.getMatchandOpponentOfPlayer(username)

    if(match<>0):
        response = 'SRVOK||{"message": "You are playing a match", "opponent": "'+str(opponent.username)+'", "matchid": "'+str(match.id)+'" }'
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
                    response = 'SRVERR||{"message": "No active user to play. You are added to waiting list. Wait or make another choice"}'
                else:
                    response = 'SRVERR||{"message": "Player could not add to waiting list"}'
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
                response = 'SRVOK||{"message": "Successful", "opponent": "'+str(opponentusername)+'", "matchid": "'+str(matchid)+'" }'
    return response

def pcplay(csocket,manager,username, matchid):
    print("PCPLAY command received")
    gameid, board= manager.getInitialGameBoard(matchid)
    if(gameid>0):
        response = 'SRVOK||{"gameid":"'+str(gameid)+'", "board": "'+ str(board)+'"}'
    return response

def pcthrowdice(csocket, manager, username, gameid):
    print("PCTHROWDICE command sent")
    dice_1 = random.randrange(1,6)
    dice_2 = random.randrange(1,6)
    dice = str(dice_1) + ""+ str(dice_2)
    ret = manager.setDice(username, gameid, dice_1, dice_2)
    if (ret):
        response = 'SRVOK||{"message": "Successful", "dice": "'+str(dice)+'", "gameid": "'+str(gameid)+'" }'
    else:
        response = 'SRVERR||{"message": "Error occured while getting dice"}'
    return response

def srvackusers(csocket, manager, username, gameid, response):
    print("Acknowledment sent to players and watchers when PCTHROWDICE or PCSENDMOVE command received")
    users=manager.getUsersByGameId(gameid)
    return users

def pcsendmove(csocket, manager, username, gameid, dice, move):
    print("PCSENDMOVE command received")
    board= manager.sendMove(username, gameid, dice, move)
    if (board):
        response = 'SRVOK||{"message": "Successful", "move": "'+str(move)+'", "gameid": "'+str(gameid)+'", "board": "'+ str(board)+'" }'
    else:
        response = 'SRERR||{"message": "Error occured while sending move"}'
    return response

def pcwrongmovealert(csocket, manager, username, gameid):
    print("PCWRONGMOVEALERT command received")

def srvackwrongmove(username,ip,gameid,previousgameboard):
    print("SRVACKWRONGMOVE command sent")

def pcreqwatch(csocket, manager, username, gameid):
    print("PCREQWATCH command received")

def pcwatch(csocket, manager, username, gameid):
    print("PCWATCH command received")

def srvhbeat(csocket, manager):
    print("SRVHBEAT  command sent")




