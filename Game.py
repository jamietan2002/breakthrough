import copy
import Player


# generates initial state
def generate_new_board(size):
    board = [
        ['B']*size, ['B']*size,  # 2 black rows
        ['_']*size, ['_']*size,  # 2 empty rows
        # ['_']*size, ['_']*size,    # 2 more empty rows # TODO Make size adjustable
        ['W']*size, ['W']*size,  # 2 white rows
    ]
    return board


def invert_board(curr_board, in_place=True):
    """ Inverts the board by modifying existing values if in_place is set to True,
    or creating a new board with updated values if in_place is set to False"""
    board = curr_board
    if not in_place:
        board = copy.deepcopy(curr_board)
    board.reverse()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'W':
                board[i][j] = 'B'
            elif board[i][j] == 'B':
                board[i][j] = 'W'
    return board


def print_board(board):
    """Prints the board"""
    horizontal_rule = '+' + ('-' * 5 + '+') * len(board)
    for i in range(len(board)):
        print(horizontal_rule)
        print('|  ' + '  |  '.join(' ' if board[i][j] == '_' else board[i][j] for j in range(len(board))) + '  |')
    print(horizontal_rule)


def print_board2(board):
    """Prints the board"""
    horizontal_rule = '+' + ('-'*3 + '+') * len(board)
    for i in range(len(board)):
        print(horizontal_rule)
        print('| ' + ' | '.join(' ' if board[i][j] == '_' else board[i][j] for j in range(len(board))) + ' |')
    print(horizontal_rule)


# checks if a move made for black is valid or not. Move source: from_ [row, col], move destination: to_ [row, col]
def is_valid_move(board, from_, to_):
    if from_ is None or to_ is None:
        return False
    if board[from_[0]][from_[1]] != 'B':  # if move not made for black
        return False
    elif (to_[0] < 0 or to_[0] >= len(board)) or (to_[1] < 0 or to_[1] >= len(board)):  # if move takes pawn outside the board
        return False
    elif to_[0] != (from_[0]+1):  # if move takes more than one step forward
        return False
    elif to_[1] > (from_[1]+1) or to_[1] < (from_[1]-1):  # if move takes beyond left/ right diagonal
        return False
    elif to_[1] == from_[1] and board[to_[0]][to_[1]] != '_':  # if pawn to the front, but still move forward
        return False
    elif ((to_[1] == from_[1]+1) or (to_[1] == from_[1]-1)) and board[to_[0]][to_[1]] == 'B':  # if black pawn to the diagonal or front, but still move forward
        return False
    else:
        return True


def state_change(curr_board, from_, to_, in_place=True):
    """ Updates the board configuration by modifying existing values if in_place is set to True,
    or creating a new board with updated values if in_place is set to False"""
    board = curr_board
    if not in_place:
        board = copy.deepcopy(curr_board)
    if is_valid_move(board, from_, to_):
        board[from_[0]][from_[1]] = '_'
        board[to_[0]][to_[1]] = 'B'
    return board


def is_game_over(board):
    """Returns True if game is over"""
    if any(  # If a piece has reached the opposite end of the board
        board[len(board) - 1][i] == 'B' or
        board[0][i] == 'W'
        for i in range(len(board))
    ):
        return True

    w_count, b_count = 0, 0  # If a player has run out of pieces
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 'B':
                b_count += 1
            elif board[i][j] == 'W':
                w_count += 1
    if w_count == 0 or b_count == 0:
        return True

    return False


# game playing function. Takes in the initial board
def play(player1, player2, board):
    colours = [BLACK, WHITE] = 'Black', 'White'
    players = [player1, player2]
    move = 0

    # Game runs
    while not is_game_over(board):
        player = players[move % 2]
        colour = colours[move % 2]

        if isinstance(player, Player.Player):
            src, dst = player.get_move(board, colour)
        else:
            if colour == WHITE:
                invert_board(board)
            src, dst = player.get_move(board)

        if not is_valid_move(board, src, dst):
            src, dst = generate_random_move(board)
            if is_valid_move(board, src, dst):
                print(f"{colour} returned invalid or no move. Making random move...")
            else:
                return f"{colour} has no possible moves"
        state_change(board, src, dst)  # make the move on the board
        if colour == WHITE:
            invert_board(board)
        move += 1

    # If is_game_over() immediately fails. Should never happen
    if move == 0:
        return "Game failed to start: Game state invalid"

    # Winner found
    print(f"The game concluded in {move} moves")
    print_board(board)  # Shows the final game board
    print_board2(board)
    return f"{colour} wins with {player.get_random_moves()} random moves"


def generate_random_move(board):
    """Finds the first available valid move for black. Returns None if no move can be found"""
    from_, to_ = [0, 0], [0, 0]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'B':
                from_[0], from_[1] = i, j
                to_[0] = from_[0] + 1
                to_[1] = from_[1]
                if is_valid_move(board, from_, to_):
                    return from_, to_
                to_[1] = from_[1] + 1
                if is_valid_move(board, from_, to_):
                    return from_, to_
                to_[1] = from_[1] - 1
                if is_valid_move(board, from_, to_):
                    return from_, to_
    return None


class Naive:

    def __init__(self):
        self.random_moves = 0

    def get_move(self, board):
        self.random_moves += 1
        return generate_random_move(board)

    def get_random_moves(self):
        return self.random_moves
