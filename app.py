from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import Game

# Create the FastAPI app and the game instance
app = FastAPI()
game = Game()


# A helper class to ensure proper data typing for POST requests
class MoveData(BaseModel):
    x: int
    y: int
    nx: int
    ny: int


class PlaceData(BaseModel):
    x: int
    y: int


class RemoveData(BaseModel):
    x: int
    y: int


class ComputerMoveData(BaseModel):
    depth: int


def get_game_state_dict():
    """Helper function to create a JSON-friendly game state dictionary."""
    return {
        "board": game.board,
        "player": game.player,
        "placed": game.placed,
        "white": game.white,
        "black": game.black,
        "white_lost": game.white_lost,
        "black_lost": game.black_lost,
        "history_length": len(game.history),
        "active_game": game.active_game,
    }


# --- File serving endpoints ---
@app.get("/")
async def get_ui():
    """Serves the main HTML file."""
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    """Serves the CSS file."""
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    """Serves the JavaScript file."""
    return FileResponse("script.js")


# --- Game interaction endpoints ---

@app.get("/get_game_state")
async def get_game_state():
    """Returns the full current state of the game."""
    return {"status": "ok", "state": get_game_state_dict()}


@app.post("/start")
async def start():
    """Starts a new game."""
    game.start()
    return {"status": "ok", "state": get_game_state_dict(), "message": "New game started!"}


@app.post("/place")
async def place(data: PlaceData):
    """
    Handles placing a piece on the board.
    Returns game state and a message.
    """
    success = game.place(data.x, data.y)
    mill = False
    message = 'Invalid placement.'

    if success:
        mill = game.check_mill(data.x, data.y, game.player)
        message = 'Piece placed successfully.'

    state = get_game_state_dict()
    state['action_required'] = 'remove' if success and mill else None

    if success and not mill:
        game.switch()
        state['player'] = game.player
        message += f" It is now Player {game.player}'s turn."

    if success and game.check_win():
        state['message'] = f"Player {'B' if game.player == 'W' else 'W'} wins!"
        state['active_game'] = False

    return {"status": "ok" if success else "error", "state": state, "message": message}


@app.post("/move")
async def move(data: MoveData):
    """
    Handles moving a piece.
    Returns game state and a message.
    """
    success = game.move(data.x, data.y, data.nx, data.ny)
    mill = False
    message = 'Invalid move.'

    if success:
        mill = game.check_mill(data.nx, data.ny, game.player)
        message = 'Piece moved successfully.'

    state = get_game_state_dict()
    state['action_required'] = 'remove' if success and mill else None

    if success and not mill:
        game.switch()
        state['player'] = game.player
        message += f" It is now Player {game.player}'s turn."

    if success and game.check_win():
        state['message'] = f"Player {'B' if game.player == 'W' else 'W'} wins!"
        state['active_game'] = False

    return {"status": "ok" if success else "error", "state": state, "message": message}


@app.post("/remove_piece")
async def remove_piece(data: RemoveData):
    """
    Handles removing an opponent's piece after a mill is formed.
    Returns game state and a message.
    """
    success = game.remove_piece(data.x, data.y, game.player)
    message = 'Invalid piece to remove.'

    if success:
        message = 'Piece removed successfully.'
        # Check for win after piece is removed
        if game.check_win():
            message = f"Player {game.player} wins!"
            game.active_game = False
        else:
            game.switch()

    state = get_game_state_dict()
    state['player'] = game.player
    # The winner is now determined by the check_win() call
    state['winner'] = game.player if not game.active_game else None

    return {"status": "ok" if success else "error", "state": state, "message": message}


@app.post("/undo")
async def undo():
    """Undoes the last move."""
    success = game.undo()
    message = 'Move undone.' if success else 'Cannot undo.'
    state = get_game_state_dict()
    return {"status": "ok" if success else "error", "state": state, "message": message}


@app.post("/computer_move")
async def computer_move(data: ComputerMoveData):
    """Makes a move for the computer."""
    success = game.computer_move(data.depth)
    message = 'Computer made a move.' if success else 'Computer could not find a valid move.'

    if success:
        if game.check_win():
            message = f"Player {game.player} wins!"
            game.active_game = False
        else:
            game.switch()

    state = get_game_state_dict()
    state['player'] = game.player
    state['winner'] = game.player if game.check_win() else None

    return {"status": "ok" if success else "error", "state": state, "message": message}


@app.get("/get_opponent_pieces")
async def get_opponent_pieces(player: str):
    """
    Gets the list of opponent pieces that can be removed.
    Used for the "remove" phase after a mill.
    """
    opponent_pieces = game.get_opponent_pieces(player)
    return {"status": "ok", "pieces": opponent_pieces}
