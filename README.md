# Chess Engine in PyQt
This chess engine was designed for the purposes of a final project for ECE 1895: Junior Design Fundamentals at the University of Pittsburgh's Swanson School of Engineering. It is a fully functional chess game that can be played between two human players on one local device.

## How It Works
### UI
The overall UI is comprised of a 8x8 chessboard and a "new game" button. The chessboard will host the actual game and have interactive functionality for playing the game, with chess squares lighting up for possible movesets and for indicators regarding checks. Pop-up widgets will also appear for promotions (which will be interactive) and for checkmates/stalemates, indicating who won if there is a winner.

### Chessboard
Each chessboard is comprised of 64 squares lined up 8x8. The 8x8 board can also be identified by the labels on the left hand side and the top side of the board, with the rows being identified in reverse row by the letter and the columns being identified by the corresponding number.

### Square
Each square is a QPushButton that can be toggleable if it contains a piece and has valid moves and is that piece's color's turn. Every adjacent square is a different color from each other to allow for a more checker-esque feel.

### Chesspiece
The chesspiece class will store the information for a chesspiece, including the type of chesspiece, the color of the chesspiece, the position of the chesspiece, and how many moves it has gone. It will also contain a method for obtaining all the possible moves depending on the type of chesspiece.

## How to Run
- In the terminal, run `python chess.py`. The UI comprising of the chessboard a "new game" button will then pop up, which will then be ready to play for the two users.
- Once a promotion occurs, a pop-up widget will appear, with 4 buttons indicating 4 pieces that a pawn can be promoted to. Clicking the button indicating whichever piece will correspond to the piece that will be promoted
- Whenever, the "new game" button is pressed, the chessboard will reset to its original position, where white will make a first move. This can be pressed at any point during the game, but will be particularly useful, especially for when a game ends on a checkmate or a stalemate.
- When a checkmate or a stalemate occurs, a popup widget will appear indicating the result of the game and the winner of the game (if there is one). Afterwards, a game can be restarted by either re-running the application or clicking the "new game" button again.