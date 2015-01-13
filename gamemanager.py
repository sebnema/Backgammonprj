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
            if (id == str(g.id)):
                return g
                break
        return 0

    def move(self,pfrom,pto):
        board = backgammon.Board.from_points((pfrom, pto))
        return board

    def getInitialGameBoard(self,matchid):
        match = self.getMatchById(matchid)
        gameid = 0
        if(match>0):
            if (match.currentgameid >0):
                game = self.getGameById(match.currentgameid)

                gameid=game.game_number
            else:
                game = backgammon.Game()
                match.games.append(game)
                gameid=game.game_number

        if (game>0):
            match.currentgameid = game.game_number
            match.state = "Playing"
            board = game.state.board

            return gameid,board
        return 0,0

    def getActiveMatches(self):
        agames = []
        for m in self.matches:
            if isinstance(m,backgammon.Match):
                if (m.state == "Playing" or m.state == "Starting"):
                    agames.append(m)
        return agames

    def getMatchandOpponentOfPlayer(self, username):
        amatches = self.getActiveMatches()
        for m in amatches:
            if isinstance(m,backgammon.Match):
                player1 = m.players[0]
                player2 = m.players[1]
                if isinstance(player1,user.User):
                    if (player1.username == username):
                        return m,player2
                if isinstance(player2,user.User):
                    if (player2.username == username):
                        return m,player1
        return 0,0


    def setDice(self,player, gameid, d1,d2):
        game = self.getGameById(gameid)
        if (game>0):
            rollactivity=backgammon.GameActivityRoll(player,d1,d2)
            if isinstance(game,backgammon.Game):
                game.moves.append(rollactivity)
                game.dice = rollactivity.dice
                return 1
        return 0

    def getGameById(self,gameid):
        amatches = self.getActiveMatches()
        for m in amatches:
            if isinstance(m,backgammon.Match):
                for g in m.games:
                    if isinstance(g,backgammon.Game):
                        if (str(g.game_number) == str(gameid)):
                            return g
        return 0

    def getUsersByGameId(self, gameid):
        users=[]
        match = 0
        amatches = self.getActiveMatches()
        for m in amatches:
            if isinstance(m,backgammon.Match):
                for g in m.games:
                    if isinstance(g,backgammon.Game):
                        if (str(g.game_number) == str(gameid)):
                            match = m

        if isinstance(match,backgammon.Match):
            users = match.players + match.watchers
            return users
        return 0

    def sendMove(self,username,gameid,move):
         game = self.getGameById(gameid)
         moveobj = backgammon.Move(game.state.board,move)
         gameactivitymove=backgammon.GameActivityMove(username,moveobj)
         gameactivitymove.apply(game.state)
         game.moves.append(gameactivitymove)
         return game.state.board


