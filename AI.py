import utils
import time
import copy
import signal

import utils
import time
import signal
class PlayerAI:
    def __init__(self):
        self.mintbl= {}
        self.maxtbl={}
        self.start = 0
    
    def make_move(self, board):
    
        '''
        This is the function that will be called from main.py
        Your function should implement a minimax algorithm with 
        alpha beta pruning to select the appropriate move based 
        on the input board state. Play for black.
        Parameters
        ----------
        self: object instance itself, passed in automatically by Python
        board: 2D list-of-lists
        Contains characters 'B', 'W', and '_' representing
        Black pawns, White pawns and empty cells respectively
        
        Returns
        -------
        Two lists of coordinates [row_index, col_index]
        The first list contains the source position of the Black pawn 
        to be moved, the second list contains the destination position
        '''
        ################
        # Starter code #
        ################
        def signal_handler(signum, frame):
            raise TimeoutError
        signal.signal(signal.SIGALRM, signal_handler)
        signal.setitimer(signal.ITIMER_REAL, 2.99)
        a = float('-inf')
        b = float('inf')
        max_v = -10000
        best_action = None
        tpl = self.successors(board, "B")
        new_states = tpl[0]
        actions = tpl[1]
        for i in range(len(new_states)):
            try:
                v = self.min_value(new_states[i], 1, a, b)
                if v > max_v:
                    max_v = v
                    best_action= actions[i]
                a = max(a, v)
            except TimeoutError:
                print("urmom")
                return best_action
        return best_action 
    def max_value(self,board, total_time, a, b):
        
        board_str = str(board)
        if board_str in self.maxtbl:
            return self.maxtbl[board_str]
        if utils.is_game_over(board) or total_time > 3:
            return self.utility(board)
        v = -1000000
        for new_state in self.successors(board, "B")[0]:
            v = max(v, self.min_value(new_state, total_time+1, a, b))
            a = max(v, a)
            if v >= b:
                break
        
        self.maxtbl[board_str] = v
        return v
    
    def min_value(self,board, total_time, a, b):
        
        board_str = str(board)
        if board_str in self.mintbl:
            return self.mintbl[board_str]
        if utils.is_game_over(board) or total_time > 3:
            return self.utility(board)
        v = 1000000
        for new_state in self.successors(board, "W")[0]:
            v = min(v, self.max_value(new_state, total_time+1, a, b))
            b = min(b, v)
            if v <= a:
                break
        self.mintbl[board_str] = v   
        return v 
    def utility(self, board):
        #minimize total distance 
        #depth 3, 21 moves, Black(Student agent) win; Random move made by Black(Student agent): 0;
        # val = 0
        # for i in range(len(board)):
        #     for j in range(len(board[i])):
        #         if board[i][j] == 'B':
        #              val += i
        #         if board[i][j] == 'W':
        #             val -= (utils.ROW - i)
        # return val
        #give weights 
        val = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'B':
                    val += i
                    #higher weight to inner columns
                    if j > 0 or j < utils.COL - 1:
                        val += 1
                if board[i][j] == 'W':
                    val -= (utils.ROW - i)
                    if j > 0 or j < utils.COL - 1:
                        val -= 2
        return val
        #depth 4, 29 moves, Black(Student agent) win; Random move made by Black(Student agent): 6;
        #minimize total distance with different weights
        # sum = 0
        # for i in range(utils.ROW):
        #      for j in range(utils.COL):
        #          if board[i][j] == 'B':
        #              sum += i**2
        # return sum
        #depth 4, 41 moves, Black(Student agent) win; Random move made by Black(Student agent): 6;
        wcount, bcount = 0, 0
        for i in range(utils.ROW):
            for j in range(utils.COL):
                if board[i][j] == 'B':
                    bcount+=1
                elif board[i][j] == 'W':
                    wcount+=1
        return bcount-wcount
        #wtf white wins??
        # minimize total vertical distance of all blacks from goal row 
        # d = 0
        # for i in range(utils.ROW):
        #     for j in range(utils.COL):
        #         if board[i][j] == 'B':
        #             d += utils.ROW - i
        # return 1/d
        #depth 4, 55 moves, Black(Student agent) win; Random move made by Black(Student agent): 4;
        minimum = 100
        for i in range(utils.ROW):
             for j in range(utils.COL):
                 if board[i][j] == 'B':
                     minimum = min(utils.ROW - i, minimum)
        return 1/minimum
        
        
    def successors(self, board, turn):
        
        new_states = []
        actions = []
        
        if turn == "W":
            board = utils.invert_board(board, False)
        def add_state(src, dst):
            temp = copy.deepcopy(board)
            utils.state_change(temp, src, dst)
            if turn == "W":
                temp = utils.invert_board(temp, False)
        
            new_states.append(temp)
            actions.append([src,dst])
        
        for r in reversed(range(len(board))):
            for c in reversed(range(len(board[r]))):
                src = [r, c]
                dst = [r+1, c]
                if board[r][c] == 'B':
                    if utils.is_valid_move(board, src, dst): #move forward
                        add_state(src, dst)
                    dst = [r+1, c+1]
                    if utils.is_valid_move(board, src, dst): #move diagonal left
                        add_state(src, dst)
                    dst = [r+1, c-1]
                    if utils.is_valid_move(board, src, dst): #move diagonal right
                        add_state(src, dst)
       
        return new_states, actions
    
class PlayerNaive:
    ''' A naive agent that will always return the first available valid move '''
    def make_move(self, board):
        return utils.generate_rand_move(board)


##########################
# Game playing framework #
##########################
if __name__ == "__main__":
    
    # public test case 1
    # res1 = utils.test([['B', 'B', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', '_', '_', '_', '_'], ['_', 'W', 'W', 'W', 'W', 'W'], ['W', 'W', 'W', 'W', 'W', 'W']], PlayerAI())
    # assert(res1 == True)

    # # public test case 2
    # res2 = utils.test([['_', 'B', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', '_', '_', '_', '_'], ['W', 'W', 'W', 'W', 'W', 'W'], ['_', '_', 'W', 'W', 'W', 'W']], PlayerAI())
    # assert(res2 == True)

    # # public test case 3
    # res3 = utils.test([['_', '_', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', 'W', '_', '_', '_'], ['_', 'W', 'W', 'W', 'W', 'W'], ['_', '_', '_', 'W', 'W', 'W']], PlayerAI())
    # assert(res3 == True)

    # template code for question 2 and question 3
    # generates initial board
    board = utils.generate_init_state()
    # # game play
    res = utils.play(PlayerAI(), PlayerNaive(), board) # PlayerNaive() will be replaced by a baby agent in question 2, or a base agent in question 3
    print(res) # BLACK wins means your agent wins. Passing the test case on Coursemology means your agent wins.
