import backgammon
import Queue
import user

class GameManager(object):
    users=[]
    matches = []
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
        for usr in self.waitinglist.queue:
            if (username == usr):
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

    def getOpponentFromWaitingList(self):
        if (len(self.waitinglist.queue)>0):
            return self.waitinglist.get()
        return 0

    def createNewMatch(self,player,opponent):
        newmatch = backgammon.Match(player,opponent)
        self.matches.append(newmatch)
        return newmatch.id

    def getMatchById(self, id):
        for g in self.matches:
            if (id == g.id):
                return g
                break
        return 0

    def createNewGame(self, match):
        moves=[]
        game = backgammon.Game(moves) # TODO
        #all_moves = [
            # '24/21 24/23', '24/20', '24/21 8/7', '24/21 6/5',
            # '24/23 13/10', '24/23 8/5', '24/23 6/3',
            # '13/9', '13/10 8/7', '13/10 6/5',
            # '8/5 8/7', '8/4', '8/5 6/5',
            # '8/7 6/3',
            # '6/3 6/5', '6/2'
            # ]
        match.games.append(game)
        match.state = "Playing"
        return game
    def move(self,pfrom,pto):
        board = backgammon.Board.from_points((pfrom, pto))
        return board

    def getInitialGameBoard(self,username,matchid):
        match = self.getMatchById(matchid)
        game = self.createNewGame(match)
        board = backgammon.initialPosition
        return game.game_number,board

    def getActiveMatches(self):
        agames = []
        for m in self.matches:
            if isinstance(m,backgammon.Match):
                if (m.state == "Playing"):
                    agames.append(m)
        return agames

    def getActiveMatchandOpponentOfPlayer(self, username):
        amatches = self.getActiveMatches()
        for m in self.amatches:
            if isinstance(m,backgammon.Match):
                player1 = m.players[0]
                player2 = m.players[1]
                if isinstance(player1,user.User):
                    if (player1.username == username):
                        return m,player1
                if isinstance(player2,user.User):
                    if (player2.username == username):
                        return m,player2
        return 0