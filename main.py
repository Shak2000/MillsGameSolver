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
        [(0, 0), (3, 0), (6, 0)],
        [(1, 1), (3, 1), (5, 1)],
        [(2, 2), (3, 2), (4, 2)],
        [(0, 3), (1, 3), (2, 3)],
        [(4, 3), (5, 3), (6, 3)],
        [(2, 4), (3, 4), (4, 4)],
        [(1, 5), (3, 5), (5, 5)],
        [(0, 6), (3, 6), (6, 6)],
        [(0, 0), (0, 3), (0, 6)],
        [(1, 1), (1, 3), (1, 5)],
        [(2, 2), (2, 3), (2, 4)],
        [(3, 0), (3, 1), (3, 2)],
        [(3, 4), (3, 5), (3, 6)],
        [(4, 2), (4, 3), (4, 4)],
        [(5, 1), (5, 3), (5, 5)],
        [(6, 0), (6, 3), (6, 6)]
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
                [[self.board[i][j] for j in range(7)] for i in range(7)],
                self.placed,
                self.white,
                self.black,
                self.white_lost,
                self.black_lost
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
        if self.get_piece_count(self.player) > 3 and (nx, ny) not in self.adjacent[(x, y)]:
            return False
        self.history.append((
            [[self.board[i][j] for j in range(7)] for i in range(7)],
            self.placed,
            self.white,
            self.black,
            self.white_lost,
            self.black_lost
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
                    else:
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
            return True
        return False


def main():
    print("Welcome to the Mill Game Solver!")


if __name__ == "__main__":
    main()
