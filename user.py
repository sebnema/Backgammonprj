class User:
    #user_id=0
    username=0
    ip=0
    activematchid=""
    socket=0
    handshake=0
    state=""

    def __init__(self, socket, username, ip="", matchid=-1,state=""):
        #self.user_id = user_id
        self.username = username
        self.ip = ip
        self.activematchid = matchid
        self.socket = socket
        self.state=state


