import Game
import Minimax
import Player


def main():
    # Create board and players
    board = Game.generate_new_board(size=6)
    minimax = Minimax.Minimax(depth=3, timeout=5)
    minimax2 = Minimax.Minimax(depth=3, timeout=5)
    player = Player.Player()

    # Start the game
    # Available players: player, minimax, Game.Naive
    # The player must always be the first parameter. Two AI can still play against each other.
    result = Game.play(player, minimax, board)
    print(result)


if __name__ == "__main__":
    main()

