import socket
import commands
import backgammon
from sys import version_info

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
z
ip = socket.gethostname()
port = 9898
s.connect((ip,port))

commands.clientsend(s, "PCCONN", '{"username": "' + username + '", "ip": "' + ip + '", "serverip": "'+ serverip +'", "serverport": "' + serverport + '"}')
# end of Screen 1

while True:
    v = s.recv(1024)
    if(v != ""):
        response=commands.clientprotocolparser(s,commands.lastsentclientcommand, v)
        print(response)
    else:
        s.close()
