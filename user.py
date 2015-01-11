class User:
    #user_id=0
    username=0
    ip=0
    gameid=0
    socket=0
    handshake=0

    def __init__(self, socket, username, ip="", gameid=-1):
        #self.user_id = user_id
        self.username = username
        self.ip = ip
        self.activegameid = gameid
        self.socket = socket

    def setgameid(self,gameid):
        self.activegameid = gameid

