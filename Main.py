import Game
import Minimax
import Player


def main():
    # Create board and players
    board = Game.generate_new_board(size=8)
    minimax = Minimax.Minimax(depth=4, timeout=120)
    player = Player.Player()

    # Start the game
    result = Game.play(player, Game.Naive(), board)  # Available players: player, minimax, Game.Naive
    print(result)


if __name__ == "__main__":
    main()

