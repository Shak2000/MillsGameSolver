# Mills Game Solver

A web-based implementation of the classic Nine Men's Morris (Mills) board game with an AI opponent using minimax algorithm.

## Features

- **Interactive Web Interface**: Modern, responsive UI with visual game board
- **AI Opponent**: Intelligent computer player using minimax algorithm with alpha-beta pruning
- **Game Phases**: Complete implementation of placing, moving, and flying phases
- **Mill Detection**: Automatic detection of mills (three pieces in a row)
- **Undo Functionality**: Step back through game history
- **Adjustable AI Difficulty**: Configure minimax search depth (1-5 levels)
- **Real-time Game State**: Live updates of piece counts and game status

## Game Rules

Nine Men's Morris is played in three phases:

### Phase 1: Placing (0-18 pieces placed)
- Players alternate placing pieces on empty intersections
- Each player has 9 pieces to place
- Form mills (3 pieces in a row) to remove opponent pieces

### Phase 2: Moving (after all 18 pieces placed)
- Move pieces to adjacent empty intersections
- Continue forming mills to remove opponent pieces
- When a player has only 3 pieces left, they can "fly" to any empty spot

### Phase 3: End Game
- Game ends when a player has fewer than 3 pieces or cannot move
- The other player wins

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup
1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Project Structure

```
mills-game/
├── app.py              # FastAPI web server and API endpoints
├── main.py             # Core game logic and AI implementation
├── index.html          # Web interface HTML
├── styles.css          # CSS styling for the game board
├── script.js           # Client-side JavaScript logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## File Descriptions

### Backend Files
- **`main.py`**: Contains the `Game` class with complete Mills game logic, minimax AI, and command-line interface
- **`app.py`**: FastAPI server providing REST API endpoints for the web interface

### Frontend Files
- **`index.html`**: Main web page with game board and controls
- **`styles.css`**: Modern styling with hover effects and responsive design
- **`script.js`**: Handles user interactions, board updates, and API communication

## API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Serves the main HTML page |
| `/get_game_state` | GET | Returns current game state |
| `/start` | POST | Starts a new game |
| `/place` | POST | Places a piece during placing phase |
| `/move` | POST | Moves a piece during moving phase |
| `/remove_piece` | POST | Removes opponent piece after mill |
| `/undo` | POST | Undoes the last move |
| `/computer_move` | POST | Triggers AI move with specified depth |
| `/get_opponent_pieces` | GET | Gets removable opponent pieces |

## AI Implementation

The computer opponent uses:
- **Minimax Algorithm**: Evaluates game positions up to specified depth
- **Alpha-Beta Pruning**: Optimizes search performance
- **Strategic Priorities**:
  1. Form mills when possible
  2. Block opponent's potential mills
  3. Use minimax evaluation for optimal moves

### Evaluation Function
- Piece count advantage: +10 points per piece difference
- Two-in-a-row formations: +5 points each
- Win/loss positions: ±1000 points

## Usage

### Web Interface
1. Click "Restart Game" to begin
2. Click empty intersections to place/move pieces
3. Use "Computer Move" with desired difficulty (depth 1-5)
4. "Undo Last Move" to step back in game history

### Command Line
Run `python main.py` for a terminal-based version with the same game logic.

### Controls
- **Placing Phase**: Click empty spots to place pieces
- **Moving Phase**: Click your piece, then click destination
- **Mill Formation**: Automatically prompts to remove opponent piece
- **Computer Difficulty**: Adjust depth (1=easy, 5=hard)

## Technical Details

### Board Representation
- 7x7 grid with 24 valid positions
- Adjacency mapping for legal moves
- 16 possible mill lines (rows, columns, squares)

### Game State Management
- Complete move history for undo functionality
- Separate tracking of pieces on board vs. pieces lost
- Phase detection (placing/moving/flying)

### Web Technology
- **Backend**: FastAPI with Python
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Custom CSS with modern design patterns
- **Communication**: RESTful API with JSON

## Development

To modify or extend the game:

1. **Game Logic**: Edit `main.py` - the `Game` class contains all rules
2. **AI Behavior**: Modify the minimax implementation and evaluation function
3. **Web Interface**: Update `script.js` for new features, `styles.css` for appearance
4. **API**: Add new endpoints in `app.py`

## License

This project is proprietary software. All rights reserved under copyright.

## Contributing

Contributions welcome! Areas for improvement:
- Enhanced AI strategies
- Multiplayer support
- Game statistics tracking
- Mobile app version
- Tournament mode
