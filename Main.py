import Game
import Minimax


def main():
    # Create board and players
    board = Game.generate_new_board()
    # player = Player()
    minimax = Minimax.Minimax(depth=4, timeout=120)
    # Start the game
    result = Game.play(Game.Naive(), Game.Naive(), board)
    print(result)


if __name__ == "__main__":
    main()
