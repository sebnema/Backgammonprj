import json
import Queue
import backgammon as bg
from enumerate import enumerate_moves

class User():
    def __init__(self, username, ip, gameid=-1):
        self.username = username
        self.ip = ip
        self.gameid=gameid


def enumerate_move1(board, d, at_most=25):
    """Generate all legal moves for a single dieroll. at_most limits
    the highest move considered. The function yields (from, to), board
    where from and to are the points moved from and to, and board is
    the final board position."""
    bearing_off = all(board[i] <= 0 for i in xrange(7, 26))
    for p in xrange(at_most, 0, -1):
        # Men on bar: don't allow any move that's not from the bar
        if p < 25 and board[25] > 0: break
        # No men on this point: don't allow move
        if board[p] <= 0: continue
        # Don't allow a move onto a point where opponent has men
        if p - d > 0 and board[p - d] < -1: continue
        # Moving off exactly; only allowed if no men above 6 point.
        if p - d == 0 and not bearing_off: continue
        # Moving off inexactly: only allowed if bearing off, and no men
        # above our point.
        if p - d < 0 and not bearing_off: continue
        if p - d < 0 and any(board[i] > 0 for i in xrange(p + 1, 7)):
            continue
        # Make a board for the new position
        b_ret = list(board)
        # Remove the moved man
        b_ret[p] -= 1
        # Add the moved man to its new square (unless it's bearing off)
        if p - d > 0:
            # Deal with hit first
            if b_ret[p - d] == -1:
                # We've hit: move the hit man to the bar
                b_ret[p - d], b_ret[0] = 0, b_ret[0] - 1
            b_ret[p - d] += 1
        yield (p, max(0, p - d)), b_ret

def testOptionalHit():
    "Check optional hit is reported with and without hit."
    board = bg.Board.from_points((6, 1), (5, -1))
    moves = ['6/5*/3', '6/3']
    dice0 = 2
    dice1 = 1

    for d0, d1 in ((dice0, dice1), (dice1, dice0)):
        for ft0, b0 in enumerate_move1(board, d0):
            for ft1, b1 in enumerate_move1(b0, d1, ft0[0]):
                b1 = tuple(b1)
                #if b1 not in enumerate.found_boards:
                #    enumerate.found_boards.add(b1)
                #    yield bg.Move(board, ft0, ft1), bg.Board(b1)

if __name__ == "__main__":

    moves2 = testOptionalHit()

    listone = [1,2,3]
    listtwo = [4,5,6]
    mergedlist = listone + listtwo

    user1 = User("serbs","sss",334)
    user2 = User("serbs","sss")

    my_queue = Queue.Queue(maxsize=0)
    print len(my_queue.queue)

    my_queue.put(user1)
    my_queue.put(user2)
    my_queue.put("1")
    my_queue.put("2")
    my_queue.put("3")
    print my_queue.get()
    my_queue.task_done()





def fromjson(val):
    #E.g. val is {"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}
    data = json.loads(val)
    return data
    #array = json.load(val)
    #return array

def jsonTest():

    python_object = {'some_text': 'my text',
                     'some_number': 12345,
                     'null_value': None,
                     'some_list': [1,2,3]}
    # here we are converting python object to json string
    json_string = json.dumps(python_object)
    # json_string = '{"some_list": [1, 2, 3], "some_text": "my text",
    #                 "some_number": 12345, "null_value": null}'
    # api converts a python dictionary to json object and vice versa
    # At this point we have a json_string in our hands. Now lets convert it back to pyton structure
    new_python_object = json.loads(json_string)
    # new_python_object = {u'some_list': [1, 2, 3], u'some_text': u'my text',
    #                      u'some_number': 12345, u'null_value': None}

    json_string='{"name":"Product-1","quantity":1,"price":12.50}'
    val = json.loads(json_string)
    #{u'name': u'Product-1', u'price': 12.5, u'quantity': 1}


    word = "This is some random text"
    word = 'PCCONN|{"username": "Joe", "ip": "11.11.11.11", "serverip": "10.24.56.78", "serverport": "9898"}'
    words2 = word.split("|")

    #json_string='{"username":"Joe","ip":"11.11.11.11","serverip":"10.24.56.78", "serverport": "9898"}'
    #val = json.loads(json_string)

    val = fromjson(words2[1])
    var = "ww"
