import sys
import copy
import math


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
        (3, 2): [(2, 2), (4, 2), (3, 1)],
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
                if all(self.board[py][px] == player for px, py in line):
                    return True
        return False

    def get_opponent_pieces(self, player):
        opponent = 'B' if player == 'W' else 'W'
        pieces = []
        for y in range(7):
            for x in range(7):
                if self.board[y][x] == opponent:
                    pieces.append((x, y))

        # If all opponent pieces are in mills, they are all removable
        if all(self.check_mill(x, y, opponent) for x, y in pieces):
            return pieces

        # Otherwise, only pieces not in a mill are removable
        return [(x, y) for x, y in pieces if not self.check_mill(x, y, opponent)]

    def remove_piece(self, x, y, player):
        opponent = 'B' if player == 'W' else 'W'
        if not (x, y) in self.adjacent:
            return False
        if self.board[y][x] != opponent:
            return False

        if (x, y) not in self.get_opponent_pieces(player):
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
        if self.placed >= 18:
            # A player wins if their opponent has fewer than 3 pieces OR has no valid moves.
            if self.get_piece_count(opponent) < 3:
                return True
            if not self.has_valid_moves(opponent):
                return True
        return False

    def has_valid_moves(self, player):
        if self.placed < 18:
            return True  # In placing phase, there's always a move if there are empty spots

        piece_count = self.get_piece_count(player)
        if piece_count < 3:
            return False  # This is a loss condition

        # Flying rule
        if piece_count == 3:
            empty_spots = 0
            for y in range(7):
                for x in range(7):
                    if self.board[y][x] == '*' and (x, y) in self.adjacent:
                        empty_spots += 1
            return empty_spots > 0

        # Normal moving
        for y in range(7):
            for x in range(7):
                if self.board[y][x] == player:
                    for nx, ny in self.adjacent.get((x, y), []):
                        if self.board[ny][nx] == '*':
                            return True
        return False

    def undo(self):
        if len(self.history) > 0:
            state = self.history.pop()
            self.board, self.placed, self.white, self.black, self.white_lost, self.black_lost, self.player = state
            return True
        return False

    def get_unblocked_two_in_a_rows(self, player):
        two_in_a_rows = []
        for line in self.lines:
            player_pieces = 0
            empty_spot = None
            for x, y in line:
                if self.board[y][x] == player:
                    player_pieces += 1
                elif self.board[y][x] == '*':
                    empty_spot = (x, y)
            if player_pieces == 2 and empty_spot is not None:
                two_in_a_rows.append(line)
        return two_in_a_rows

    def evaluate_board(self):
        if self.check_win():
            # The current player has made a move that caused the opponent to lose
            return 1000 if self.player == 'W' else -1000

        score = 0
        # More weight for piece difference
        score += (self.white - self.black) * 10
        # Less weight for 2-in-a-rows
        score += len(self.get_unblocked_two_in_a_rows('W')) * 5
        score -= len(self.get_unblocked_two_in_a_rows('B')) * 5
        return score

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.check_win():
            return self.evaluate_board(), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_possible_moves():
                temp_game = copy.deepcopy(self)
                new_pos = self.apply_move(temp_game, move)

                eval_after_move = 0
                if temp_game.check_mill(new_pos[0], new_pos[1], temp_game.player):
                    best_removal_eval = -math.inf
                    # After a mill, the other player will make a move.
                    # So we find the removal that leads to the best state for us (the maximizer).
                    for rem_x, rem_y in temp_game.get_opponent_pieces(temp_game.player):
                        removal_game = copy.deepcopy(temp_game)
                        removal_game.remove_piece(rem_x, rem_y, temp_game.player)
                        removal_game.switch()
                        evaluation, _ = removal_game.minimax(depth - 1, alpha, beta, False)
                        best_removal_eval = max(best_removal_eval, evaluation)
                    eval_after_move = best_removal_eval if best_removal_eval > -math.inf else temp_game.evaluate_board()
                else:
                    temp_game.switch()
                    eval_after_move, _ = temp_game.minimax(depth - 1, alpha, beta, False)

                if eval_after_move > max_eval:
                    max_eval = eval_after_move
                    best_move = move
                alpha = max(alpha, eval_after_move)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:  # Minimizing player
            min_eval = math.inf
            for move in self.get_possible_moves():
                temp_game = copy.deepcopy(self)
                new_pos = self.apply_move(temp_game, move)

                eval_after_move = 0
                if temp_game.check_mill(new_pos[0], new_pos[1], temp_game.player):
                    best_removal_eval = math.inf
                    for rem_x, rem_y in temp_game.get_opponent_pieces(temp_game.player):
                        removal_game = copy.deepcopy(temp_game)
                        removal_game.remove_piece(rem_x, rem_y, temp_game.player)
                        removal_game.switch()
                        evaluation, _ = removal_game.minimax(depth - 1, alpha, beta, True)
                        best_removal_eval = min(best_removal_eval, evaluation)
                    eval_after_move = best_removal_eval if best_removal_eval < math.inf else temp_game.evaluate_board()
                else:
                    temp_game.switch()
                    eval_after_move, _ = temp_game.minimax(depth - 1, alpha, beta, True)

                if eval_after_move < min_eval:
                    min_eval = eval_after_move
                    best_move = move
                beta = min(beta, eval_after_move)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_possible_moves(self):
        moves = []
        if self.placed < 18:
            for y in range(7):
                for x in range(7):
                    if self.board[y][x] == '*' and (x, y) in self.adjacent:
                        moves.append((x, y))
        else:
            player_pieces = []
            for y in range(7):
                for x in range(7):
                    if self.board[y][x] == self.player:
                        player_pieces.append((x, y))

            if self.get_piece_count(self.player) == 3:  # Flying
                for x, y in player_pieces:
                    for ny in range(7):
                        for nx in range(7):
                            if self.board[ny][nx] == '*' and (nx, ny) in self.adjacent:
                                moves.append(((x, y), (nx, ny)))
            else:  # Normal move
                for x, y in player_pieces:
                    for nx, ny in self.adjacent.get((x, y), []):
                        if self.board[ny][nx] == '*':
                            moves.append(((x, y), (nx, ny)))
        return moves

    def computer_move(self, depth):
        opponent = 'B' if self.player == 'W' else 'W'

        # Priority 1: If possible, form a mill.
        mill_moves = []
        for move in self.get_possible_moves():
            temp_game = copy.deepcopy(self)
            new_pos = self.apply_move(temp_game, move)
            if temp_game.check_mill(new_pos[0], new_pos[1], self.player):
                mill_moves.append(move)

        if mill_moves:
            # If multiple ways to form a mill, pick the best one via minimax
            best_move = None
            best_score = -math.inf if self.player == 'W' else math.inf

            for move in mill_moves:
                game_after_move = copy.deepcopy(self)
                self.apply_move(game_after_move, move)

                # Simulate the best removal to score the position
                temp_score, _ = game_after_move.minimax(depth - 1, -math.inf, math.inf, self.player == 'B')

                if self.player == 'W':
                    if temp_score > best_score:
                        best_score = temp_score
                        best_move = move
                else:
                    if temp_score < best_score:
                        best_score = temp_score
                        best_move = move

            if best_move:
                new_pos = self.apply_move(self, best_move)
                print(f"Computer forms a mill at {new_pos}.")
                self.handle_computer_mill_removal(self, depth)
                return True

        # Priority 2: Block an opponent's unblocked 2-in-a-row.
        opponent_twos = self.get_unblocked_two_in_a_rows(opponent)
        if opponent_twos:
            blocking_spot = None
            for line in opponent_twos:
                for x, y in line:
                    if self.board[y][x] == '*':
                        blocking_spot = (x, y)
                        break
                if blocking_spot:
                    break

            if blocking_spot:
                # Find a move to that blocking spot
                for move in self.get_possible_moves():
                    is_placing = self.placed < 18
                    dest = move if is_placing else move[1]
                    if dest == blocking_spot:
                        new_pos = self.apply_move(self, move)
                        print(f"Computer blocks opponent's 2-in-a-row at {new_pos}.")
                        return True

        # Priority 3: Use minimax for a general move.
        print("Computer is thinking...")
        _, best_move = self.minimax(depth, -math.inf, math.inf, self.player == 'W')

        if best_move:
            new_pos = self.apply_move(self, best_move)
            print(f"Computer moves to {new_pos}.")
            if self.check_mill(new_pos[0], new_pos[1], self.player):
                print("Computer formed a mill!")
                self.handle_computer_mill_removal(self, depth)
            return True

        return False

    def get_coordinates(self, prompt):
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

    def handle_mill_removal(self, game):
        while True:
            print("Available pieces to remove:", game.get_opponent_pieces(game.player))
            rx, ry = game.get_coordinates("Enter coordinates of the opponent's piece to remove (x y): ")
            if rx is not None and ry is not None:
                if game.remove_piece(rx, ry, game.player):
                    print(f"Opponent's piece at ({rx}, {ry}) removed.")
                    break
                else:
                    print(
                        "Invalid piece to remove. The piece might not exist, or it is in a mill when other pieces are "
                        "not.")

    def handle_computer_mill_removal(self, game, depth):
        """
        Decides which piece the computer should remove after forming a mill,
        following a specific priority list.
        """
        opponent = 'B' if game.player == 'W' else 'W'
        removable_pieces = game.get_opponent_pieces(game.player)
        if not removable_pieces:
            return

        piece_to_remove = None

        # Priority 1: Remove a piece from an opponent's unblocked 2-in-a-row
        opponent_twos = game.get_unblocked_two_in_a_rows(opponent)
        if opponent_twos:
            for line in opponent_twos:
                for piece in line:
                    if piece in removable_pieces:
                        piece_to_remove = piece
                        break
                if piece_to_remove:
                    break

        # Priority 2: Use minimax to determine the best piece to remove
        if not piece_to_remove:
            best_score = -math.inf if game.player == 'W' else math.inf

            for rem_x, rem_y in removable_pieces:
                removal_game = copy.deepcopy(game)
                removal_game.remove_piece(rem_x, rem_y, game.player)
                removal_game.switch()

                is_maximizing = (removal_game.player == 'W')
                score, _ = removal_game.minimax(depth - 1, -math.inf, math.inf, is_maximizing)

                if game.player == 'W':
                    if score > best_score:
                        best_score = score
                        piece_to_remove = (rem_x, rem_y)
                else:
                    if score < best_score:
                        best_score = score
                        piece_to_remove = (rem_x, rem_y)

        # Fallback if no piece is chosen
        if not piece_to_remove and removable_pieces:
            piece_to_remove = removable_pieces[0]

        if piece_to_remove:
            print(f"Computer removes opponent's piece at {piece_to_remove}.")
            game.remove_piece(piece_to_remove[0], piece_to_remove[1], game.player)

    def apply_move(self, game, move):
        """
        Internal helper to apply a move to a game instance.
        It correctly handles both placing and moving phases.
        Returns the coordinates of the new piece location for mill checking.
        """
        if game.placed < 18:
            # Placing phase: move is a single tuple (x, y)
            nx, ny = move
            game.place(nx, ny)
            return nx, ny
        else:
            # Moving phase: move is a nested tuple ((from_x, from_y), (to_x, to_y))
            (x, y), (nx, ny) = move
            game.move(x, y, nx, ny)
            return nx, ny


def main():
    def print_board(curr_game):
        visual_board = [list(line) for line in curr_game.visual]
        for cy in range(7):
            for cx in range(7):
                if (cx, cy) in curr_game.adjacent:
                    vx, vy = cx * 2, cy * 2
                    visual_board[vy][vx] = curr_game.board[cy][cx]
        for row in visual_board:
            print("".join(row))

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
            print(f"Player W has {game.white} pieces on the board (lost {game.white_lost}).")
            print(f"Player B has {game.black} pieces on the board (lost {game.black_lost}).")
            print(f"Total placed pieces: {game.placed}/18")
            print("1. Take an action")
            print("2. Let computer play")
            print("3. Undo a move")
            print("4. Restart the game")
            print("5. Quit")
            choice = input("Enter your choice: ")

            action_taken = False
            if choice == '1':
                if game.placed < 18:
                    print("Placing phase.")
                    x, y = game.get_coordinates("Enter coordinates to place your piece (x y): ")
                    if x is not None and y is not None and game.place(x, y):
                        print(f"Piece placed at ({x}, {y}).")
                        if game.check_mill(x, y, game.player):
                            print("You formed a mill! You can remove an opponent's piece.")
                            game.handle_mill_removal(game)
                        action_taken = True
                    else:
                        print("Invalid placement. Please try again.")
                else:
                    print("Moving phase.")
                    x, y = game.get_coordinates("Enter source coordinates (x y): ")
                    nx, ny = game.get_coordinates("Enter destination coordinates (x y): ")
                    if x is not None and y is not None and nx is not None and ny is not None and game.move(x, y, nx,
                                                                                                           ny):
                        print(f"Piece moved from ({x}, {y}) to ({nx}, {ny}).")
                        if game.check_mill(nx, ny, game.player):
                            print("You formed a mill! You can remove an opponent's piece.")
                            game.handle_mill_removal(game)
                        action_taken = True
                    else:
                        print("Invalid move. Please try again.")

            elif choice == '2':
                try:
                    depth = int(input("Enter minimax depth: "))
                    if game.computer_move(depth):
                        action_taken = True
                    else:
                        print("Computer could not find a valid move.")
                        print_board(game)
                        print(f"Player {game.player} has no moves and loses!")
                        print(f"Player {'B' if game.player == 'W' else 'W'} wins!")
                        game.active_game = False

                except ValueError:
                    print("Invalid depth. Please enter an integer.")

            elif choice == '3':
                if game.undo():
                    print("Move undone.")
                else:
                    print("Cannot undo. No moves in history.")
            elif choice == '4':
                game.start()
                print("Game restarted.")
            elif choice == '5':
                print("Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

            if action_taken:
                if game.check_win():
                    print_board(game)
                    print(f"Player {game.player} wins!")
                    game.active_game = False
                else:
                    game.switch()


if __name__ == "__main__":
    main()
