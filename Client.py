import socket
import commands
import backgammon
from sys import version_info


global lastsentclientcommand
lastsentclientcommand=""

s = socket.socket()

#Screen 1: Connect to Server
py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
if py3:
  username = input("Please enter username: ")
  serverip = input("Please enter server ip: ")
  serverport = input("Please enter server port: ")
else:
  username = raw_input("Please enter username: ")
  serverip = raw_input("Please enter server ip: ")
  serverport = raw_input("Please enter server port: ")

#TODO ip ve port sorunu
ip = socket.gethostname()
serverip  = ip
port = 9898 #int(serverport)


# end of Screen 1

def parseInput(input):
    cmd = input.split()
    if (input.__contains__("PCREQPLAY")):
        lastsentclientcommand = "PCREQPLAY"
        #PCREQPLAY sebnema
        username = cmd[1]
        ret ='{"username": "' + username + '}'
    return ret

def connect(s,username,ip,serverip,serverport):
    print("Conneting...")
    s.connect((serverip ,port))
    lastsentclientcommand = "PCCONN"
    commands.clientsend(s, lastsentclientcommand, '{"username": "' + username + '", "ip": "' + ip + '", "serverip": "'+ serverip +'", "serverport": "' + serverport + '"}')


while True:
    input = raw_input("$ ")
    if (input.lower() == "connect"):
        connect(s,username,ip,serverip,serverport)
    else:
        ret = parseInput(input)
        commands.clientsend(s, lastsentclientcommand, ret)

    v = s.recv(1024)
    if(v != ""):
        response=commands.clientprotokolparser(lastsentclientcommand, v)
        print(response)
    else:
        s.close()
