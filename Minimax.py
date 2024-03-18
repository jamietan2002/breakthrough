import Game
import copy
import multiprocessing


class Minimax:

    def __init__(self, depth=3, timeout=3):
        self.min_tbl = {}
        self.max_tbl = {}
        self.timeout = timeout
        self.random_moves = 0
        self.depth = depth

    def get_move(self, board):
        """Calculates a move using minimax"""
        src, dst = None, None
        result_queue = multiprocessing.Queue()
        board_copy = copy.deepcopy(board)
        mp = multiprocessing.Process(target=self.get_move_job_func, args=(board_copy, result_queue))

        mp.start()
        mp.join(self.timeout)
        exit_code = mp.exitcode
        if mp.is_alive():
            mp.terminate()
            print("Minimax hit the time limit. Returning random move")
            return Game.generate_random_move(board)
        if exit_code is None:
            # src, dst = result_queue.get()
            del result_queue
        elif exit_code == 1:
            e = result_queue.get()
            del result_queue
            print(f"minimax returned err={e} while searching for move")
            return None
        elif exit_code == 0:
            src, dst = result_queue.get()
            del result_queue
        else:
            del result_queue

        try:
            isValid = Game.is_valid_move(board, src, dst)
        except IndexError:
            isValid = False
        if not isValid:
            print("Invalid move found. Returning random move")
            self.random_moves += 1
            return Game.generate_random_move(board)
        return src, dst

    def get_move_job_func(self, board, queue):
        """Starts the find_move() function and puts the result into the queue. Should be called with multithreading"""
        try:
            src, dst = self.find_move(board)
            # returns [i1, j1], [i2, j2] -> pawn moves from position [i1, j1] to [i2, j2]
            queue.put((src, dst))
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            queue.put(e)
            exit(1)
        return

    def find_move(self, board):
        a = float('-inf')
        b = float('inf')
        max_v = -10000
        best_action = None
        tpl = self.successors(board, "B")  # Makes a list of possible moves from this state
        new_states = tpl[0]
        actions = tpl[1]
        depth = self.depth
        while True:
            try:
                for i in range(len(new_states)):  # Iterates over the possible moves
                    v = self.min_value(new_states[i], depth, a, b)
                    if v > max_v:
                        max_v = v
                        best_action = actions[i]
                    a = max(a, v)
                # print("B: ", best_action) #print for visualization
                return best_action
            except TimeoutError:
                return best_action

    def max_value(self, board, depth, a, b):
        board_str = str(board)
        if board_str in self.max_tbl:
            return self.max_tbl[board_str]
        if Game.is_game_over(board) or depth == 0:
            return self.utility(board)
        v = -1000000
        for new_state in self.successors(board, "B")[0]:
            v = max(v, self.min_value(new_state, depth - 1, a, b))
            if v >= b:  # beta cutoff
                return v
            a = max(v, a)  # update alpha
        self.max_tbl[board_str] = v
        return v

    def min_value(self, board, depth, a, b):
        board_str = str(board)
        if board_str in self.min_tbl:  # If the board state has already been evaluated, return the value
            return self.min_tbl[board_str]
        if Game.is_game_over(board) or depth == 0:  # If this is max depth or victory, return the utility of this state
            return self.utility(board)
        v = 1000000
        for new_state in self.successors(board, "W")[0]:
            v = min(v, self.max_value(new_state, depth - 1, a, b))
            if v <= a:  # alpha cutoff
                return v
            b = min(b, v)  # update beta
        self.min_tbl[board_str] = v
        return v

    def utility(self, board):
        # give weights
        val = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'B':
                    val += i
                    if i == len(board) - 1:
                        val += 1000  # If the move will win the game
                    # higher weight to inner columns
                    if j > 0 or j < len(board) - 1:
                        val += 1
                if board[i][j] == 'W':
                    val -= (len(board) - i)
                    if j > 0 or j < len(board) - 1:
                        val -= 2
        return val

    def successors(self, board, turn):
        new_states = []
        actions = []

        if turn == "W":
            board = Game.invert_board(board, False)

        def add_state(board, src, dst):
            temp = copy.deepcopy(board)
            temp = Game.state_change(temp, src, dst)
            new_states.append(temp)
            actions.append([src, dst])

        for r in reversed(range(len(board))):
            for c in reversed(range(len(board[r]))):
                src = [r, c]
                dst = [r + 1, c]
                if board[r][c] == 'B':
                    if Game.is_valid_move(board, src, dst):  # move forward
                        add_state(board, src, dst)

                    dst = [r + 1, c + 1]
                    if Game.is_valid_move(board, src, dst):  # move diagonal left
                        add_state(board, src, dst)

                    dst = [r + 1, c - 1]
                    if Game.is_valid_move(board, src, dst):  # move diagonal right
                        add_state(board, src, dst)
        return new_states, actions

    def get_random_moves(self):
        return self.random_moves
