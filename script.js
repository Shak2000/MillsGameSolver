// script.js - Client-side logic for the Mills Game UI.
document.addEventListener('DOMContentLoaded', () => {
    // UI element references
    const boardPoints = document.querySelector('.board-points');
    const playerTurnDisplay = document.getElementById('playerTurn');
    const gameMessage = document.getElementById('gameMessage');
    const whitePiecesCount = document.getElementById('whitePieces');
    const blackPiecesCount = document.getElementById('blackPieces');
    const whiteLostCount = document.getElementById('whiteLost');
    const blackLostCount = document.getElementById('blackLost');
    const restartButton = document.getElementById('restartButton');
    const undoButton = document.getElementById('undoButton');
    const computerMoveButton = document.getElementById('computerMoveButton');
    const depthInput = document.getElementById('depthInput');

    // Mappings for board coordinates to visual positions, updated for the new board layout
    const coordsToPos = {
        '0,0': { top: '5%', left: '5%' },
        '3,0': { top: '5%', left: '50%' },
        '6,0': { top: '5%', left: '95%' },
        '0,3': { top: '50%', left: '5%' },
        '1,3': { top: '50%', left: '25%' },
        '2,3': { top: '50%', left: '40%' },
        '4,3': { top: '50%', left: '60%' },
        '5,3': { top: '50%', left: '75%' },
        '6,3': { top: '50%', left: '95%' },
        '0,6': { top: '95%', left: '5%' },
        '3,6': { top: '95%', left: '50%' },
        '6,6': { top: '95%', left: '95%' },
        '1,1': { top: '25%', left: '25%' },
        '3,1': { top: '25%', left: '50%' },
        '5,1': { top: '25%', left: '75%' },
        '1,5': { top: '75%', left: '25%' },
        '3,5': { top: '75%', left: '50%' },
        '5,5': { top: '75%', left: '75%' },
        '2,2': { top: '40%', left: '40%' },
        '3,2': { top: '40%', left: '50%' },
        '4,2': { top: '40%', left: '60%' },
        '2,4': { top: '60%', left: '40%' },
        '3,4': { top: '60%', left: '50%' },
        '4,4': { top: '60%', left: '60%' },
    };

    // Client-side game state
    let gameState = {};
    let clientState = {
        action: 'placing', // 'placing', 'moving', 'removing', 'none'
        selectedPiece: null, // {x, y}
    };

    // --- Core UI Update Functions ---

    /**
     * Renders the game board and updates all status indicators based on the game state.
     * @param {object} state - The game state object from the server.
     */
    function updateUI(state) {
        gameState = state;

        // Clear existing board points
        boardPoints.innerHTML = '';
        const pointsWithPieces = [];

        // Create new points and pieces
        for (const coordKey in coordsToPos) {
            const [x, y] = coordKey.split(',').map(Number);

            const point = document.createElement('div');
            point.className = 'point';
            point.style.top = coordsToPos[coordKey].top;
            point.style.left = coordsToPos[coordKey].left;
            point.dataset.x = x;
            point.dataset.y = y;

            // Add piece if present
            const pieceType = gameState.board[y][x];
            if (pieceType !== '*') {
                const piece = document.createElement('div');
                piece.className = `piece ${pieceType === 'W' ? 'white' : 'black'}`;
                point.appendChild(piece);
                pointsWithPieces.push(point);
            }

            point.addEventListener('click', handlePointClick);
            boardPoints.appendChild(point);
        }

        // Update status display
        if (gameState.winner) {
            playerTurnDisplay.textContent = `Game Over`;
            gameMessage.textContent = `Player ${gameState.winner} wins!`;
        } else {
            playerTurnDisplay.textContent = gameState.active_game ? `Player ${gameState.player}'s Turn` : `Game Over`;
            gameMessage.textContent = gameState.message || '';
        }

        // Update piece counts
        whitePiecesCount.textContent = gameState.white;
        blackPiecesCount.textContent = gameState.black;
        whiteLostCount.textContent = gameState.white_lost;
        blackLostCount.textContent = gameState.black_lost;

        // Manage client-side state
        if (!gameState.active_game) {
            clientState.action = 'none';
        } else if (gameState.action_required === 'remove') {
            clientState.action = 'removing';
            gameMessage.textContent = `Player ${gameState.player} formed a mill! Select an opponent's piece to remove.`;
        } else if (gameState.placed < 18) {
            clientState.action = 'placing';
        } else {
            clientState.action = 'moving';
        }
    }

    // --- Event Handlers ---

    /**
     * Handles clicks on the game board points.
     * @param {Event} event - The click event.
     */
    async function handlePointClick(event) {
        if (!gameState.active_game || clientState.action === 'none') return;

        const x = parseInt(event.currentTarget.dataset.x);
        const y = parseInt(event.currentTarget.dataset.y);
        const pieceType = gameState.board[y][x];
        let response = null;
        let success = false;

        if (clientState.action === 'placing') {
            if (pieceType === '*') {
                response = await postData('/place', { x, y });
                success = response.status === 'ok';
            } else {
                gameMessage.textContent = 'This spot is already taken!';
            }
        } else if (clientState.action === 'moving') {
            // First click selects a piece
            if (!clientState.selectedPiece && pieceType === gameState.player) {
                clientState.selectedPiece = { x, y };
                event.currentTarget.classList.add('selected');
                gameMessage.textContent = `Selected piece at (${x}, ${y}). Now choose a destination.`;
            }
            // Second click moves the selected piece
            else if (clientState.selectedPiece && pieceType === '*') {
                const { x: fx, y: fy } = clientState.selectedPiece;
                response = await postData('/move', { x: fx, y: fy, nx: x, ny: y });
                success = response.status === 'ok';
                // Remove selected class from old piece position
                const selectedPoint = document.querySelector(`.point[data-x="${clientState.selectedPiece.x}"][data-y="${clientState.selectedPiece.y}"]`);
                if (selectedPoint) selectedPoint.classList.remove('selected');
                clientState.selectedPiece = null;
            }
            // Clicks on another player's piece or an invalid spot
            else {
                gameMessage.textContent = 'Invalid move. Please select one of your pieces and an empty spot.';
                if (clientState.selectedPiece) {
                    const selectedPoint = document.querySelector(`.point[data-x="${clientState.selectedPiece.x}"][data-y="${clientState.selectedPiece.y}"]`);
                    if (selectedPoint) selectedPoint.classList.remove('selected');
                }
                clientState.selectedPiece = null;
            }
        } else if (clientState.action === 'removing') {
            const opponent = gameState.player === 'W' ? 'B' : 'W';
            if (pieceType === opponent) {
                const removablePiecesResponse = await fetch(`/get_opponent_pieces?player=${gameState.player}`);
                const removablePiecesData = await removablePiecesResponse.json();
                const removablePieces = removablePiecesData.pieces;

                const isRemovable = removablePieces.some(p => p[0] === x && p[1] === y);

                if (isRemovable) {
                    response = await postData('/remove_piece', { x, y });
                    success = response.status === 'ok';
                    if (success) {
                        clientState.action = 'moving'; // Transition back to moving
                    }
                } else {
                    gameMessage.textContent = "That piece is in a mill and cannot be removed (unless all opponent pieces are in mills). Please select another piece.";
                }
            } else {
                gameMessage.textContent = "You must remove an opponent's piece. Please click on one of their pieces.";
            }
        }

        if (response) {
            updateUI(response.state);
        }
    }

    /**
     * Fetches the game state from the server.
     */
    async function fetchGameState() {
        const response = await fetch('/get_game_state');
        if (response.ok) {
            const data = await response.json();
            updateUI(data.state);
        } else {
            console.error('Failed to fetch game state.');
            gameMessage.textContent = 'Error: Could not connect to the server.';
        }
    }

    /**
     * Sends a POST request to the server with JSON data.
     * @param {string} url - The API endpoint URL.
     * @param {object} data - The data to send.
     * @returns {Promise<object>} A promise that resolves to the JSON response.
     */
    async function postData(url = '', data = {}) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
            return response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            gameMessage.textContent = 'A network error occurred. Please try again.';
            return { status: 'error' };
        }
    }

    // --- Button Event Listeners ---
    restartButton.addEventListener('click', async () => {
        const response = await postData('/start');
        if (response.status === 'ok') {
            updateUI(response.state);
        }
    });

    undoButton.addEventListener('click', async () => {
        const response = await postData('/undo');
        if (response.status === 'ok') {
            updateUI(response.state);
        }
    });

    computerMoveButton.addEventListener('click', async () => {
        const depth = parseInt(depthInput.value, 10);
        if (!isNaN(depth) && depth > 0) {
            gameMessage.textContent = 'Computer is thinking...';
            const response = await postData('/computer_move', { depth });
            if (response.status === 'ok') {
                updateUI(response.state);
            }
        } else {
            gameMessage.textContent = 'Please enter a valid depth (a positive integer).';
        }
    });

    // Automatically start a new game on page load
    postData('/start').then(response => {
        if (response.status === 'ok') {
            updateUI(response.state);
        }
    });
});
