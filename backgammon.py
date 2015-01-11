import graphics
import binascii
import copy
import itertools
import Queue
import uuid

class Match(object):
    "A backgammon match"
    def __init__(self,player1,player2):
        self.id = uuid.uuid4()
        self.state = "Started"
        self.players = [player1, player2]
        self.games = []
    def report(self):
        "Generate lines describing the match"
        yield 'Match to %d' % self.length
        for g in self:
            yield ''
            for line in g.report():
                yield line
    @property
    def games(self):
        return list(self.games)
    def __iter__(self):
        for g in self.games:
            yield g
    def addGame(self,game):
        self.games.append(game)

class Game(object):
    "A single game of backgammon."
    def __init__(self, moves, score=(0, 0), players=None):
        self.score = score
        self._moves = list(moves)
        self.players = players or ('Player0', 'Player1')
        self.game_number = uuid.uuid4()

    def replay(self):
        "Generate pre-state, move and post-state for each move in the game."
        game_state = GameState()
        for move in self:
            pre_state = copy.copy(game_state)
            move.apply(game_state)
            yield pre_state, move, game_state

    def report(self):
        "Return a log of all moves in the game"
        def comma_and(g):
            "Join strings together with ', ' but use 'and' for the last one."
            g = list(g)
            if len(g) == 1: return g[0]
            return ', '.join(g[:-1]) + ' and ' + g[-1]

        for p, moves in itertools.groupby(self, lambda x:x.player):
            yield 'Player %d %s.' % (p, comma_and(map(str, moves)))

    @property
    def result(self):
        for m in self._moves:
            if isinstance(m, GameMoveWin):
                return m.player, m.points
        return None

    def __iter__(self):
        for m in self._moves:
            yield m


class GameState(object):
    "The state of a game being played."
    def __init__(self):
        self.board = initialPosition
        self.dice = None
    _keys = ['board', 'dice']
    @property
    def kwargs(self):
        return dict((k, getattr(self, k)) for k in self._keys)

class GameMove(object):
    "Base class for the things a player can do in a game."
    @property
    def report(self):
        return 'Player %d %s.' % (self.player, self)
    @property
    def _report(self):
        return str(self)
    def __str__(self):
        return 'Erroneous move type %s' % type(self)
    def apply(self, game_state):
        game_state.dice = None
        #game_state.offer = None
    @property
    def action(self):
        "A short version of the type (eg 'roll')"
        return type(self).__name__.rpartition('GameMove')[2].lower()


class GameMoveRoll(GameMove):
    "A player rolls the dice."
    def __init__(self, player, d0, d1):
        self.player = player
        self.dice = d0, d1
    def __str__(self):
        return 'rolls %d%d' % self.dice
    def apply(self, game_state):
        game_state.dice = self.dice


class GameMoveMove(GameMove):
    "A player moves some stones."
    def __init__(self, player, move):
        self.player = player
        self.move = move
    def __str__(self):
        if self.move: return 'moves %s' % self.move
        else: return 'cannot move'
    def apply(self, game_state):
        game_state.dice = None
        game_state.board = self.move.board_after
        if self.player:
            game_state.board = game_state.board.reverse()

class GameMoveWin(GameMove):
    "A player wins the game."
    def __init__(self, player, points):
        self.player = player
        self.points = points
    def __str__(self):
        return 'wins %d point%s' % (self.points, 's' * (self.points != 1))


class Board(tuple):
    @property
    def pipcounts(board):
        "Return pipcounts for both players"
        p0, p1 = 0, 0
        for i in xrange(1, 26):
            p0 += i * board[i] * (board[i] > 0)
            p1 -= i * board[-i - 1] * (board[-i - 1] < 0)
        return p0, p1

    @property
    def positionID(self):
        "Generate a 14 character ID uniquely describing a board."
        # This encoding only works for up to 30 stone in play.
        assert sum(abs(k) for k in self) <= 30
        def bits():
            """Generate 80 bits describing the board. 0 means next
               point, and 1 means add a stone to the current point. Player 0's
               stones are described first, followed by player 1's.
               80 = (number of players) * (number of points + number of stones)
                  = 2 * (25 + 15)
               If a player has less than 15 stones on the board the total number
               of bits will be less than 80. The stream is padded with 0's
               at the end to cope with this.
            """
            for player in xrange(2):
                for i in xrange(1, 26):
                    pt = 25 - i if player else i
                    sign = -1 if player else 1
                    for j in xrange(max(self[pt] * sign, 0)):
                        yield 1
                    yield 0
            for pad in xrange(sum(self.stones_off)):
                yield 0
        # Generate the stream of bits.
        b = bits()
        # Encode the bits into 10 8-bit bytes.
        code = [chr(sum(b.next() << i for i in xrange(8))) for j in xrange(10)]
        # And base-64 encode them.
        # b2a_base64 pads to a multiple of 4 characters, and appends \n.
        # We want 14 characters (14 * 6 = 84 [6 = bit per character in base
        # 64]) so we need to throw 3 characters away from the end.
        return binascii.b2a_base64(''.join(code))[:-3]

    @staticmethod
    def from_positionID(position_id):
        "Create a board from a position ID."
        assert len(position_id) == 14
        # a2b_base64 required 4-byte padding.
        code = binascii.a2b_base64(position_id + '==')
        def bits(bytes):
            for b in map(ord, bytes):
                for i in xrange(8):
                    yield (b >> i) & 1
        i, points = 0, [0] * 26
        for b in bits(code):
            player, pt = i // 25, i % 25
            if b:
                # Bit found: add a stone to the current point.
                points[24 - pt if player else pt + 1] += (1, -1)[player]
            else:
                # No bit found: go to the next point.
                i += 1
        return Board(points)

    @classmethod
    def from_points(cls, *args):
        "Given points and number of stones, return a board structure."
        points = [0] * 26
        for (p, n) in args:
            if p < 0:
                p = 25 + p
            #assert p in xrange(0, 26)
            #assert points[p] == 0
            points[p] = n
        return cls(points)
    @property
    def stones_off(self):
        return [max(0, 15 - sum(j * i for i in self if i * j > 0))
            for j in (1, -1)]
    def reverse(self):
        """Swap the board round, producing board from other player's
        perspective"""
        return Board(-i for i in reversed(self))

    def __str__(self):
        return graphics.toString_ascii(self, False)

def all_rolls():
    "Generate all rolls, larger first"
    for d0 in xrange(1, 7):
        for d1 in xrange(1, d0 + 1):
            yield (d0, d1)

initialPosition = Board.from_points(
    (24, 2), (13, 5), (8, 3), (6, 5), (-24, -2), (-13, -5), (-8, -3), (-6, -5))


