import sys
import copy


class Game:
    visual = [
        "*─────*─────*",
        "|     |     |",
        "| *───*───* |",
        "| |   |   | |",
        "| | *─*─* | |",
        "| | |   | | |",
        "*─*─*   *─*─*",
        "| | |   | | |",
        "| | *─*─* | |",
        "| |   |   | |",
        "| *───*───* |",
        "|     |     |",
        "*─────*─────*"
    ]

    adjacent = {
        (0, 0): [(3, 0), (0, 3)],
        (3, 0): [(0, 0), (6, 0), (3, 1)],
        (6, 0): [(3, 0), (6, 3)],
        (1, 1): [(3, 1), (1, 3)],
        (3, 1): [(3, 0), (3, 2), (1, 1), (5, 1)],
        (5, 1): [(3, 1), (5, 3)],
        (2, 2): [(3, 2), (2, 3)],
        (3, 2): [(2, 2), (2, 4), (3, 1)],
        (4, 2): [(3, 2), (4, 3)],
        (0, 3): [(0, 0), (0, 6), (1, 3)],
        (1, 3): [(0, 3), (2, 3), (1, 1), (1, 5)],
        (2, 3): [(2, 2), (2, 4), (1, 3)],
        (4, 3): [(4, 2), (4, 4), (5, 3)],
        (5, 3): [(4, 3), (6, 3), (5, 1), (5, 5)],
        (6, 3): [(6, 0), (6, 6), (5, 3)],
        (2, 4): [(2, 3), (3, 4)],
        (3, 4): [(2, 4), (4, 4), (3, 5)],
        (4, 4): [(4, 3), (3, 4)],
        (1, 5): [(1, 3), (3, 5)],
        (3, 5): [(1, 5), (5, 5), (3, 4), (3, 6)],
        (5, 5): [(3, 5), (5, 3)],
        (0, 6): [(0, 3), (3, 6)],
        (3, 6): [(0, 6), (6, 6), (3, 5)],
        (6, 6): [(6, 3), (3, 6)]
    }

    lines = {
        frozenset([(0, 0), (3, 0), (6, 0)]),
        frozenset([(1, 1), (3, 1), (5, 1)]),
        frozenset([(2, 2), (3, 2), (4, 2)]),
        frozenset([(0, 3), (1, 3), (2, 3)]),
        frozenset([(4, 3), (5, 3), (6, 3)]),
        frozenset([(2, 4), (3, 4), (4, 4)]),
        frozenset([(1, 5), (3, 5), (5, 5)]),
        frozenset([(0, 6), (3, 6), (6, 6)]),
        frozenset([(0, 0), (0, 3), (0, 6)]),
        frozenset([(1, 1), (1, 3), (1, 5)]),
        frozenset([(2, 2), (2, 3), (2, 4)]),
        frozenset([(3, 0), (3, 1), (3, 2)]),
        frozenset([(3, 4), (3, 5), (3, 6)]),
        frozenset([(4, 2), (4, 3), (4, 4)]),
        frozenset([(5, 1), (5, 3), (5, 5)]),
        frozenset([(6, 0), (6, 3), (6, 6)])
    }

    def __init__(self):
        self.board = [['*' for j in range(7)] for i in range(7)]
        self.player = 'W'
        self.placed = 0
        self.white = 0
        self.black = 0
        self.white_lost = 0
        self.black_lost = 0
        self.history = []
        self.active_game = False

    def start(self):
        self.board = [['*' for j in range(7)] for i in range(7)]
        self.player = 'W'
        self.placed = 0
        self.white = 0
        self.black = 0
        self.white_lost = 0
        self.black_lost = 0
        self.history = []
        self.active_game = True

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def place(self, x, y):
        if self.placed < 18 and (x, y) in self.adjacent.keys() and self.board[y][x] == '*':
            self.history.append((
                copy.deepcopy(self.board),
                self.placed,
                self.white,
                self.black,
                self.white_lost,
                self.black_lost,
                self.player
            ))
            self.board[y][x] = self.player
            self.placed += 1
            if self.player == 'W':
                self.white += 1
            else:
                self.black += 1
            return True
        return False

    def move(self, x, y, nx, ny):
        if self.placed < 18:
            return False
        if (x, y) not in self.adjacent.keys() or self.board[y][x] != self.player:
            return False
        if self.board[ny][nx] != '*':
            return False
        if (nx, ny) not in self.adjacent.keys():
            return False
        if self.get_piece_count(self.player) > 3 and (nx, ny) not in self.adjacent.get((x, y), []):
            return False

        self.history.append((
            copy.deepcopy(self.board),
            self.placed,
            self.white,
            self.black,
            self.white_lost,
            self.black_lost,
            self.player
        ))

        self.board[y][x] = '*'
        self.board[ny][nx] = self.player
        return True

    def get_piece_count(self, player):
        if player == 'W':
            return self.white
        else:
            return self.black

    def check_mill(self, x, y, player):
        for line in self.lines:
            if (x, y) in line:
                all_same = True
                for px, py in line:
                    if self.board[py][px] != player:
                        all_same = False
                        break
                if all_same:
                    return True
        return False

    def get_opponent_pieces(self, player):
        opponent = 'B' if player == 'W' else 'W'
        pieces = []
        for y in range(7):
            for x in range(7):
                if self.board[y][x] == opponent:
                    pieces.append((x, y))

        all_in_mills = True
        for x, y in pieces:
            if not self.check_mill(x, y, opponent):
                all_in_mills = False
                break

        if all_in_mills:
            return pieces

        removable = []
        for x, y in pieces:
            if not self.check_mill(x, y, opponent):
                removable.append((x, y))
        return removable

    def remove_piece(self, x, y, player):
        opponent = 'B' if player == 'W' else 'W'
        if not (x, y) in self.adjacent:
            return False
        if self.board[y][x] != opponent:
            return False

        removable_pieces = self.get_opponent_pieces(player)
        if (x, y) not in removable_pieces:
            return False

        self.board[y][x] = '*'
        if opponent == 'W':
            self.white_lost += 1
            self.white -= 1
        else:
            self.black_lost += 1
            self.black -= 1
        return True

    def check_win(self):
        opponent = 'B' if self.player == 'W' else 'W'
        if self.placed >= 18 and self.get_piece_count(opponent) <= 2:
            return True
        if self.placed >= 18 and not self.has_valid_moves(opponent):
            return True
        return False

    def has_valid_moves(self, player):
        piece_count = self.get_piece_count(player)
        if piece_count <= 2:
            return False
        for y in range(7):
            for x in range(7):
                if self.board[y][x] == player:
                    if piece_count > 3:
                        for nx, ny in self.adjacent.get((x, y), []):
                            if self.board[ny][nx] == '*':
                                return True
                    else:  # Flying rule
                        for ny_inner in range(7):
                            for nx_inner in range(7):
                                if self.board[ny_inner][nx_inner] == '*' and (nx_inner, ny_inner) in self.adjacent:
                                    return True
        return False

    def undo(self):
        if len(self.history) > 0:
            state = self.history.pop()
            self.board = state[0]
            self.placed = state[1]
            self.white = state[2]
            self.black = state[3]
            self.white_lost = state[4]
            self.black_lost = state[5]
            self.player = state[6]
            return True
        return False


def print_board(game):
    """
    Prints the current state of the game board.
    It combines the static visual representation with the dynamic piece positions.
    """
    visual_board = [list(line) for line in game.visual]

    # Mapping from board coordinates (x, y) to visual coordinates (vx, vy)
    # The visual board is a 13x13 grid, while the game board is a 7x7 grid.
    # The relationship is generally (x,y) -> (x*2, y*2) for the visual representation.
    for y in range(7):
        for x in range(7):
            if (x, y) in game.adjacent:
                vx, vy = x * 2, y * 2
                visual_board[vy][vx] = game.board[y][x]

    for row in visual_board:
        print("".join(row))


def get_coordinates(prompt):
    """
    Helper function to get valid integer coordinates from user input.
    Handles ValueError and ensures the correct number of inputs.
    """
    try:
        coors = input(prompt).split()
        if len(coors) != 2:
            print("Invalid input. Please enter two numbers separated by a space.")
            return None, None
        x = int(coors[0])
        y = int(coors[1])
        return x, y
    except ValueError:
        print("Invalid input. Please enter integers for the coordinates.")
        return None, None


def handle_mill_removal(game):
    """
    Handles the mill removal logic, prompting the user until a valid
    opponent's piece is removed.
    """
    while True:
        rx, ry = get_coordinates("Enter coordinates of the opponent's piece to remove (x y): ")
        if rx is not None and ry is not None:
            if game.remove_piece(rx, ry, game.player):
                print(f"Opponent's piece at ({rx}, {ry}) removed.")
                break
            else:
                print("Invalid piece to remove. The piece might be in a mill, or the coordinates are invalid.")


def main():
    """
    Main function to run the Mills game loop.
    """
    game = Game()

    while True:
        if not game.active_game:
            print("\n---")
            print("No game is currently being played.")
            print("1. Start a new game")
            print("2. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                game.start()
                print("New game started.")
            elif choice == '2':
                print("Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n---")
            print_board(game)
            print(f"It's player {game.player}'s turn.")
            print(f"Player W has {game.white} pieces on the board.")
            print(f"Player B has {game.black} pieces on the board.")
            print(f"Total placed pieces: {game.placed}/18")
            print("1. Take an action")
            print("2. Undo a move")
            print("3. Restart the game")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                if game.placed < 18:
                    # Placing phase
                    print("Placing phase.")
                    x, y = get_coordinates("Enter coordinates to place your piece (x y): ")
                    if x is not None and y is not None:
                        if game.place(x, y):
                            print(f"Piece placed at ({x}, {y}).")
                            if game.check_mill(x, y, game.player):
                                print("You formed a mill! You can remove an opponent's piece.")
                                handle_mill_removal(game)

                            if game.check_win():
                                print_board(game)
                                print(f"Player {game.player} wins!")
                                game.active_game = False
                            else:
                                game.switch()
                        else:
                            print("Invalid placement. Please try again.")
                else:
                    # Moving phase
                    print("Moving phase.")
                    x, y = get_coordinates("Enter source coordinates (x y): ")
                    nx, ny = get_coordinates("Enter destination coordinates (x y): ")
                    if x is not None and y is not None and nx is not None and ny is not None:
                        if game.move(x, y, nx, ny):
                            print(f"Piece moved from ({x}, {y}) to ({nx}, {ny}).")
                            if game.check_mill(nx, ny, game.player):
                                print("You formed a mill! You can remove an opponent's piece.")
                                handle_mill_removal(game)

                            if game.check_win():
                                print_board(game)
                                print(f"Player {game.player} wins!")
                                game.active_game = False
                            else:
                                game.switch()
                        else:
                            print("Invalid move. Please try again.")
            elif choice == '2':
                if game.undo():
                    print("Move undone.")
                else:
                    print("Cannot undo. No moves in history.")
            elif choice == '3':
                game.start()
                print("Game restarted.")
            elif choice == '4':
                print("Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
