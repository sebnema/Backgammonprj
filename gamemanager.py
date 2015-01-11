import backgammon
import Queue
import user

class GameManager(object):
    users=[]
    games = []
    waitinglist = Queue.Queue(maxsize=0)

    def findUserBySocket(self, clientsocket):
        for user in self.users:
            if user.socket == clientsocket:
                return user
        return 0

    def findUserByName(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return 0

    def checkifUserExists(self, username):
        exists = 0
        for g in self.users:
            if (username == g.username):
                exists = 1
                break
        for g in self.waitinglist.queue:
            if (username == g.username):
                exists = 1
                break
        return exists

    def addToUsers(self, channel, username, ip, gameid):
        if(self.findUserByName(username)==0):
            self.users.append(user.User(channel, username, ip, gameid))
            return 1
        return 0

    def addToWaitingList(self, username):
         try:
            self.waitinglist.put(username)
            useradded=1
         except Exception as err:
            print(err.args)
            useradded=0
         return useradded

    def dequeueOpponentFromWaitingList(self,username):
        opponent = self.waitinglist.get()
        return opponent

    def createNewMatch(self,player,opponent):
        newmatch = backgammon.Match(player,opponent)
        #game = Game() # TODO
        #newmatch.addGame(game)
        return newmatch.id


    # def player(self, i):
    #     "The user object , one of the players"
    #     return self.users[i]

    # def activegames(self):
    #     # TODO filter by game state
    #     agames = []
    #     for g in self.games:
    #         if isinstance(g,backgammon.Game):
    #             if (g.gamestate == "Active"):
    #                 agames.append(g)
    #     return agames