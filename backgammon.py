import graphics
import binascii
import uuid
import re
import itertools

class Match(object):
    "A backgammon match"
    def __init__(self,player1,player2):
        self.id = uuid.uuid4()
        self.state = "Starting"
        self.players = [player1, player2]
        self.watchers = []
        self.games = []
        self.currentgameid=0
    def __iter__(self):
        for g in self.games:
            yield g

class Game(object):
    "A single game of backgammon."
    def __init__(self, moves=[], score=(0, 0), dice="00"):
        self.score = score
        self.moves = list(moves)
        self.game_number = uuid.uuid4()
        self.dice = dice
        self.state = GameState()
    @property

    def __iter__(self):
        for m in self.moves:
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

class GameActivity(object):
    "Base class for the things a player can do in a game."
    def __str__(self):
        return 'Erroneous move type %s' % type(self)
    def apply(self, game_state):
        game_state.dice = None

class GameActivityRoll(GameActivity):
    "A player rolls the dice."
    def __init__(self, player, d0, d1):
        self.player = player
        self.dice = d0, d1
    def __str__(self):
        return 'rolls %d%d' % self.dice
    def apply(self, game_state):
        game_state.dice = self.dice

class GameActivityMove(GameActivity):
    "A player moves some stones."
    def __init__(self, player, move):
        self.player = player
        self.move = move #Eg. Move object in the form of '6/5*/3'
    def __str__(self):
        if self.move: return 'moves %s' % self.move
        else: return 'cannot move'
    def apply(self, game_state):
        game_state.dice = None
        game_state.board = self.move.board_after
        if self.player:
            game_state.board = game_state.board.reverse()

class Move(object):
    # (c) Copyright 2008 Paul Hankin. All Rights Reserved.
    """An object representing a move. Constructed from a board and a
    list of basic movements, it's converted lazily to a user-readable string
    in normal backgammon notation."""
    def __init__(self, board, *from_to):
        assert all(len(m) == 2 for m in from_to)
        self._board = board
        self._from_to = from_to
    move_mult = re.compile(r'^(.*?)(\((\d)\))?$')
    move_valid = re.compile(r'((\d+|bar)(/(\d+|off|bar)\*?)+(\(\d\))? *)+')

    def __nonzero__(self):
        return len(self._from_to) > 0

    def __iter__(self):
        for m in self._from_to:
            yield m

    @property
    def board(self): return self._board
    @property
    def board_after(self):
        "Return the game board after the move is played."
        if getattr(self, '_board_after', None): # Cache
            return self._board_after
        # Create a mutable version of the board for we are going to modify it
        board = list(self._board)
        for move in self._from_to:
            if board[move[0]] <= 0: raise Exception('move exception')
            # Remove any blots we may have hit
            for w in (m for m in move if board[m] == -1 and m > 0):
                board[w], board[0] = 0, board[0] - 1
            if not all(board[w] >= 0 for w in move if w > 0):
                raise Exception('move exception')
            # Apply the move (careful - point 0 is off rather than opps bar)
            board[move[0]] -= 1
            if move[-1] > 0:
                board[move[-1]] += 1
        self._board_after = Board(board)
        return self._board_after

    @classmethod
    def from_string(cls, board, move):
        """Parse moves of the form 'a[/b\\*?]*/c\\*?(\(n\))'
        where a, b, c are 1..24 or bar or off. Each move is separated
        by spaces. Returns a Move object."""
        assert cls.move_valid.match(move), "%s is not valid" % move
        moves = move.split()
        fts = []
        for m in moves:
            # Remove *'s as they aren't necessary
            m = m.replace('*', '')
            # Separate move from multiplicity
            m = cls.move_mult.match(m)
            m, mult = m.group(1), m.group(3)
            mult = int(mult) if mult else 1
            steps = m.split('/')
            steps = map(cls._point_from_name, steps)
            for i in xrange(len(steps) - 1):
                fts.extend([(steps[i], steps[i + 1])] * mult)
        # Make sure our moves are highest-checker first.
        fts.sort(cls.move_order)
        return cls(tuple(board), *fts)
    @staticmethod
    def move_order(a, b):
        # Highest checker comes first
        if a[0] < b[0]: return 1
        if a[0] > b[0]: return -1
        # Furthest move comes first
        if a[-1] < b[-1]: return -1
        if a[-1] > b[-1]: return 1
        # Most hits comes first (or break ties using default comparison)
        return (len(b) - len(a)) or cmp(a, b)
    def str_simple(self):
        """A simple representation of the move. Each checker move is written
        out in full"""
        return ' '.join('%d/%d' % (f, t) for f, t in self._from_to)
    def __str__(self):
        if not hasattr(self, '_move'):
            self._move = self._make_move(self._board, list(self._from_to))
        return self._move
    @staticmethod
    def _point_name(x, d={0:'off', 25:'bar'}):
        "Map point numbers to names. 0 is off, 25 is the bar."
        return d.get(x, x)
    @staticmethod
    def _point_from_name(n, d={'off':0, 'bar':25}):
        "Map a string representing a point to its point number."
        return int(d.get(n, n))
    @staticmethod
    def _join_combo(moves):
        """Find and remove a combination move and return True, or
         return False if no combination exists."""
        for i in xrange(len(moves) - 1):
            for j in xrange(i + 1, len(moves)):
                if moves[i][-1] == moves[j][0]:
                    moves[i] = moves[i][:-1] + moves[j]
                    del moves[j]
                    return True
        return False
    def _nice_move(self, move, mult, hit_set, board):
        """Nicely format a single move, returning a string of the form
           eg: 24/18*/12 or 13/8 or 13/9* or 13/7(2).
        move is a list of moves a single checker makes.
        mult is the number of checkers that share this move
        hit_set is a set of points on which a hit has already been noted.
        board is the starting position"""
        comps = []
        for i, m in enumerate(move):
            if i != 0 and m != move[-1] and (board[m] != -1 or m in hit_set):
                continue
            hit = m > 0 and board[m] == -1
            if hit:
                if m in hit_set:
                    hit = False
                    assert m == move[-1]
                else:
                    hit_set.add(m)
            comps += ['%s%s' % (self._point_name(m), '*' if hit else '')]
        return '/'.join(comps) + ('' if mult == 1 else '(%d)' % mult)

    def _make_move(self, board, moves):
        moves = list(moves)
        # Join up single checker moves
        while self._join_combo(moves):
            pass
        # Combine duplicate moves together
        moves = map(lambda x:(x[0], len(list(x[1]))), itertools.groupby(moves))
        hits = set()
        return ' '.join(self._nice_move(mv, c, hits, board) for mv, c in moves)

class Board(tuple):
    # (c) Copyright 2008 Paul Hankin. All Rights Reserved.
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


