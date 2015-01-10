# Ascii board
def _stone_ascii(board, i):
    bar = (i == 0 or i == 25)
    dot = '. ' if not bar else '  '
    piece, count = ['O ', 'X '][board[i] < 0], abs(board[i])
    result = [piece] * min(5, count) + [dot] * max(0, 5 - count)
    # Replace top man with a number if there's too many men to fit.
    if count > 5: result[4] = '%-2d' % count
    # Bar men drawn upside down - first man appears near centre of board
    if bar: result = [' ' + x for x in reversed(result)]
    assert len(result) == 5, result
    return result

def toString_asciig(board, reverse_numbers=False):
    tables, nums = [None] * 4, [None] * 4
    rs = [xrange(*m) for m in ((1, 7), (7, 13), (18, 12, -1), (24, 18, -1))]
    for i, q in enumerate(rs):
        tables[i] = [' '.join(a) for a in zip(*(_stone_ascii(board, x) for x in q))]
        nums[i] = ' '.join('%-2d' % x for x in q)
    if reverse_numbers:
        nums.reverse()
    yield nums[0], 'BAR', nums[1]
    for i in xrange(5):
        yield tables[0][i], _stone_ascii(board, 0)[i], tables[1][i]
    yield ' ' * 17, '   ', ' ' * 17
    for i in xrange(4, -1, -1):
        yield tables[3][i], _stone_ascii(board, 25)[i], tables[2][i]
    yield nums[3], 'BAR', nums[2]

def toString_ascii(board, reverse_numbers=False):
    "An ascii board."
    return '\n'.join('%s | %s | %s' % x for x in toString_asciig(board, reverse_numbers))
