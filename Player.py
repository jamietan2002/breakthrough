import Game
import os


def typecheck(input, size):  # size of board determines max input. 8 is used for comments below
    if len(input) != 5:
        return False
    if ord(input[0]) not in range(97, 97+size) and ord(input[0]) not in range(65, 65+size):  # If not a-h or A-H
        return False
    if not 0 < int(input[1]) <= size:  # If not 1-8
        return False
    if ord(input[3]) not in range(97, 97+size) and ord(input[3]) not in range(65, 65+size):  # If not a-h or A-H
        return False
    if not 0 < int(input[4]) <= size:  # If not 1-8
        return False
    return True


def convert_to_move(input):
    src = [int(input[1])-1, ord(input[0]) - 65] if input[0].isupper() else [int(input[1])-1, ord(input[0]) - 97]
    dst = [int(input[4])-1, ord(input[3]) - 65] if input[3].isupper() else [int(input[4])-1, ord(input[3]) - 97]
    return src, dst


class Player:

    def get_move(self, board, colour):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        Game.print_large_board(board)
        print(f"You are {colour}. Make your move.")
        print("Format: A5 B6")
        while True:
            userInput = input()
            if typecheck(userInput, len(board)):
                src, dst = convert_to_move(userInput)
                if Game.is_valid_move(board, src, dst):
                    return src, dst
                else:
                    print("Invalid move. Try again.")
            else:
                print("Invalid input. Try again.")

    def get_random_moves(self):
        return 0

    if __name__ == '__main__':
        #str = input()
        str = 'G2 H6'
        str2 = [n for n in range(1, 8+1)]
        print(str2)
        print(str)
        print(convert_to_move(str))
        print(typecheck(str, 8))
