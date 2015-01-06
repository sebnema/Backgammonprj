import time
import random

def protocolparser(csocket, input, codelist):
    input = input.strip()
    val = input[0:3]
    if (val == "HEL"):
        csocket.send('SLT')
    elif (val == "QUI"):
        csocket.send('BYE')
    elif (val == "GET"):
        country = input[4:]
        code = codelist[country]
        if (code != ""):
            csocket.send(code)
        else:
            csocket.send('ERR')
    elif (val == "TIC"):
        csocket.send('TOC' + time.localtime())
    elif (val == '' or val == ' '):
        csocket.send('NTF')
    else:
        csocket.send('ERR')


def pcconn(username, ip):
    print("PCCONN command sent")


def pcreqplay(username, ip):
    print("PCREQPLAY command sent")


def pcplay(username, ip, gameid):
    print("PCPLAY command sent")


def pcwatch(username, ip, gameid):
    print("PCWATCH command sent")


def pcthrowdice(username, ip):
    print("PCTHROWDICE command sent")
    dice_1 = random.randrange(1,6)
    dice_2 = random.randrange(1,6)
    dice = dice_1 + dice_2


def pcsendmove(username, ip, gameid, move):
    print("PCSENDMOVE command sent")


def pcwrongmovealert(username, ip, gameid):
    print("PCWRONGMOVEALERT command sent")


def pcbearoff(username, ip, gameid, move):
    print("PCBEAROFF command sent")

def pcbearoff(username, ip, gameid, move):
    print("PCBEAROFF command sent")