import random
from copy import deepcopy

def allowed_moves(board, color):
    """
        This is the first function you need to implement.

        Arguments:
        - board: The content of the board, represented as a list of strings.
                 The length of strings are the same as the length of the list,
                 which represents a 8x8 checkers board.
                 Each string is a row, from the top row (the black side) to the
                 bottom row (white side). The string are made of five possible
                 characters:
                 - '_' : an empty square
                 - 'b' : a square with a black disc
                 - 'B' : a square with a black king
                 - 'w' : a square with a white disc
                 - 'W' : a square with a white king
                 At the beginning of the game:
                 - the top left square of a board is always empty
                 - the square on it right always contains a black disc
        - color: the next player's color. It can be either 'b' for black or 'w'
                 for white.

        Return value:
        It must return a list of all the valid moves. Please refer to the
        README for a description of what are valid moves. A move is a list of
        all the squares visited by a disc or a king, from its initial position
        to its final position. The coordinates of the square must be specified
        using (row, column), with both 'row' and 'column' starting from 0 at
        the top left corner of the board (black side).

        Example:
        >> board = [
            '________',
            '__b_____',
            '_w_w____',
            '________',
            '_w______',
            '_____b__',
            '____w___',
            '___w____'
        ]

        The top-most black disc can chain two jumps and eat both left white
        discs or jump only over the right white disc. The other black disc
        cannot move because it does produces any capturing move.

        The output must thus be:
        >> allowed_moves(board, 'b')
        [
            [(1, 2), (3, 0), (5, 2)],
            [(1, 2), (3, 4)]
        ]
    """
    board = [list(row.rstrip()) for row in board]
    w_pieces = [] ## list of all current white positions
    b_pieces = [] ## list of all current black positions
    for i in range(len(board)):
        for j in range(len(board)): 
            if board[i][j] == 'b' or board[i][j] == 'B':
                b_pieces.append((i,j)) 
            if board[i][j] == 'w' or board[i][j] == 'W':
                w_pieces.append((i,j))
                
    success = []
    
    def generate_steps(color):
        if color == 'b':
            return [(1,-1),(1,1)] ## Its coming down.

        if color == 'w':
            return [(-1,-1),(-1,1)] ## its going up.

        if color == 'B':
            return [(1,-1),(1,1),(-1,-1),(-1,1)]

        if color == 'W':
            return [(-1,1),(-1,-1),(1,1),(1,-1)]
    
    def move_single(board, a_tuple, success, color):
        current_piece = a_tuple
        for step in generate_steps(color):
            x, y = current_piece[0] + step[0], current_piece[1] + step[1]
            ## Checking for the valid moves.
            if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == '_':
                board[x][y] = board[current_piece[0]][current_piece[1]]
                board[current_piece[0]][current_piece[1]] = '_'
                if (x == 7) or (x == 0):
                    color = color.upper()
                    board[x][y] = board[x][y].upper()
                success.append([current_piece, (x, y)])   
            
    def jump(board, a_tuple, moves, success, color):
        Jump = True
        current_piece = a_tuple
        for step in generate_steps(color):
            x, y = current_piece[0] + step[0], current_piece[1] + step[1]
            if (x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] != '_' and 
                board[current_piece[0]][current_piece[1]].lower() != board[x][y].lower()):
                xp, yp = x + step[0], y + step[1]
                ## Jump will occur only when xp, yp is _
                if xp >= 0 and xp < 8 and yp >= 0 and yp < 8 and board[xp][yp] == '_':
                    board[xp][yp], temp = board[current_piece[0]][current_piece[1]], board[x][y]
                    board[current_piece[0]][current_piece[1]] = board[x][y] = '_'
                    prev = board[xp][yp]
                    
                    if (xp == 7 and color == 'b') or (xp == 0 and color == 'w'):
                        color = color.upper()
                        
                    moves.append((xp,yp))   
                    jump(board, (xp,yp), moves, success, color)
                    moves.pop()
                    board[current_piece[0]][current_piece[1]], board[x][y], board[xp][yp] = prev, temp, '_'
                    Jump = False
        if Jump and len(moves)>1: 
            success.append(deepcopy(moves)) 
         
    if color == 'b' or color == 'B':
        for i in range(len(b_pieces)):
            if board[b_pieces[i][0]][b_pieces[i][1]] == 'B':
                color = color.upper()
            boardcopy = deepcopy(board)    
            jump(boardcopy, b_pieces[i], [b_pieces[i]], success, color)
    else:
        for i in range(len(w_pieces)):
            if board[w_pieces[i][0]][w_pieces[i][1]] == 'W':
                color = color.upper()
            boardcopy = deepcopy(board)    
            jump(boardcopy, w_pieces[i], [w_pieces[i]], success, color)
    
    if len(success) > 0: 
        return success
    
    if color == 'b' or color == 'B':
        for i in range(len(b_pieces)):
            if board[b_pieces[i][0]][b_pieces[i][1]] == 'B':
                color = color.upper()
            boardcopy = deepcopy(board)        
            move_single(boardcopy, b_pieces[i], success, color)
    else:
        for i in range(len(w_pieces)):
            if board[w_pieces[i][0]][w_pieces[i][1]] == 'W':
                color = color.upper()
            boardcopy = deepcopy(board)        
            move_single(boardcopy, w_pieces[i], success, color)
    
    return success

def play(board, color):
    """
        Play must return the next move to play.
        You can define here any strategy you would find suitable.
    """
    return random_play(board, color)

def random_play(board, color):
    """
        An example of play function based on allowed_moves.
    """
    moves = allowed_moves(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
