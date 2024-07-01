
---

# Chess Engine using Pygame

## Overview
This project is a chess engine built using Python and Pygame. It includes three main components:
- `ChessMain.py`: The main driver of the application, responsible for handling user inputs and displaying the current game state.
- `ChessEngine.py`: Contains the logic for managing the game state, move generation, and validations.
- `SmartMoveFinder.py`: Implements the AI for the chess engine, including basic move evaluation and decision-making processes.

## Features
- **Human vs Human**: Play against another human on the same device.
- **Human vs AI**: Play against the computer with AI determining the best moves.
- **Move Log**: Displays the history of moves made during the game.
- **Undo/Redo Moves**: Undo and redo moves to explore different game scenarios.
- **Animations**: Smooth animations for piece movements.

## Installation
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd chess-engine-pygame
   ```

2. **Install dependencies**:
   Ensure you have Python and Pygame installed. You can install Pygame using pip:
   ```bash
   pip install pygame
   ```

3. **Download Piece Images**:
   Place the chess piece images in a directory named `Chess/images/`. The images should be named as follows: `wK.png`, `wQ.png`, `wR.png`, `wB.png`, `wN.png`, `wP.png`, `bK.png`, `bQ.png`, `bR.png`, `bB.png`, `bN.png`, `bP.png`.

## Usage
Run the main driver script to start the chess engine:
```bash
python ChessMain.py
```

### Controls
- **Mouse**: Click on a piece and then click on the destination square to move.
- **Ctrl + Z**: Undo the last move.
- **Ctrl + Y**: Redo the undone move.
- **Ctrl + R**: Restart the game.

## File Descriptions
### ChessMain.py
- Initializes Pygame and sets up the main game window.
- Loads images for the chess pieces.
- Handles user inputs (mouse clicks and key presses).
- Manages the game loop, drawing the game state, move log, and handling animations.
- Coordinates with `ChessEngine` for game state management and `SmartMoveFinder` for AI moves.

### ChessEngine.py
- Manages the game state, including the board setup, piece positions, and turn tracking.
- Implements move generation and validation, including special moves like castling, en passant, and pawn promotion.
- Keeps track of move history for undo and redo functionality.

### SmartMoveFinder.py
- Implements basic AI for the chess engine.
- Evaluates board positions and scores moves based on piece values and positions.
- Uses simple algorithms to determine the best move for the AI.

## Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
- The Pygame community for the graphics and game development framework.
- Various online resources for chess programming and AI techniques.

---