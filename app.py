from fastapi import FastAPI
from fastapi.responses import FileResponse
from main import Game

app = FastAPI()
game = Game()


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start")
async def start():
    game.start()


@app.post("/switch")
async def switch():
    game.switch()


@app.post("/place")
async def place(x, y):
    game.place(x, y)


@app.post("/move")
async def move(x, y, nx, ny):
    game.move(x, y, nx, ny)


@app.get("/get_piece_count")
async def get_piece_count(player):
    return game.get_piece_count(player)


@app.get("/check_mill")
async def check_mill(x, y, player):
    return game.check_mill(x, y, player)


@app.get("/get_opponent_pieces")
async def get_opponent_pieces(player):
    return game.get_opponent_pieces(player)


@app.post("/remove_piece")
async def remove_piece(x, y, player):
    return game.remove_piece(x, y, player)


@app.get("/check_win")
async def check_win():
    return game.check_win()


@app.get("/has_valid_moves")
async def has_valid_moves(player):
    return game.has_valid_moves(player)


@app.post("/undo")
async def undo():
    return game.undo()


@app.get("/get_unblocked_two_in_a_rows")
async def get_unblocked_two_in_a_rows(player):
    return game.get_unblocked_two_in_a_rows(player)


@app.get("/evaluate_board")
async def evaluate_board():
    return game.evaluate_board()


@app.get("/minimax")
async def minimax(depth, alpha, beta, maximizing_player):
    return game.minimax(depth, alpha, beta, maximizing_player)


@app.get("/get_possible_moves")
async def get_possible_moves():
    return game.get_possible_moves()


@app.post("/computer_move")
async def computer_move(depth):
    return game.computer_move(depth)


@app.post("/handle_computer_mill_removal")
async def handle_computer_mill_removal(curr_game, depth):
    game.handle_computer_mill_removal(curr_game, depth)


@app.post("/apply_move")
async def apply_move(curr_game, curr_move):
    game.apply_move(curr_game, curr_move)
