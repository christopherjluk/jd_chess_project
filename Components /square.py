# Square class for the chess game

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

from Components.chesspiece import Chesspiece


class Square(QPushButton):
    def __init__(self, color = "green", col = -1, row = -1):
        super(QPushButton, self).__init__()
        self.color = color
        self.contains_piece = None
        self.col = col
        self.row = row
        self.setup_square()

    def setup_square(self):
        """
        Function for setting up the square
        """
        self.setStyleSheet("background-color : " + self.color)
        self.setFixedHeight(50)
        self.setFixedWidth(50)
        self.setFont(QFont('Times', 28))
        self.setCheckable(False)

    def reset_color(self):
        """
        Function for resetting the color
        """
        self.setStyleSheet("background-color : " + self.color)

    def setup_piece(self, piece : Chesspiece):
        """
        Function for setting up the pieces on the square

        Inputs
            piece : Chesspiece
                The chesspiece
        """
        self.contains_piece = piece
        self.setCheckable(self.has_piece())
        if self.has_piece():
            self.contains_piece.set_position(self.col, self.row)
            self.setText(piece.get_pixel_image())
        else:
            self.setText("")

    def get_piece(self):
        """
        Function for getting the piece on the square

        Outputs
            self.contains_piece : Chesspiece
                The piece on the square
        """
        return self.contains_piece

    def has_piece(self):
        """
        Function will return whether the square has a piece

        Outputs
            self.contains_piece is not None : bool
                Whether the square contains a piece
        """
        return (self.contains_piece is not None)
    
    def move_piece(self):
        """
        Function will move a piece and call the corresponding function
        
        Outputs
            possible_moves : list of lists
                The list of possible moves
        """
        possible_moves = []
        if self.contains_piece is None:
            return possible_moves
        else:
            if self.contains_piece.get_piece_name() == 'pawn':
                possible_moves.append(self.contains_piece.move_pawn()[0])
                possible_moves.append(self.contains_piece.move_pawn()[1])
            elif self.contains_piece.get_piece_name() == 'rook':
                possible_moves.append(self.contains_piece.move_rook()[0])
                possible_moves.append(self.contains_piece.move_rook()[1])
                possible_moves.append(self.contains_piece.move_rook()[2])
                possible_moves.append(self.contains_piece.move_rook()[3])
            elif self.contains_piece.get_piece_name() == 'knight':
                possible_moves = self.contains_piece.move_knight()
            elif self.contains_piece.get_piece_name() == 'bishop':
                possible_moves.append(self.contains_piece.move_bishop()[0])
                possible_moves.append(self.contains_piece.move_bishop()[1])
                possible_moves.append(self.contains_piece.move_bishop()[2])
                possible_moves.append(self.contains_piece.move_bishop()[3])
            elif self.contains_piece.get_piece_name() == 'queen':
                possible_moves.append(self.contains_piece.move_queen()[0])
                possible_moves.append(self.contains_piece.move_queen()[1])
                possible_moves.append(self.contains_piece.move_queen()[2])
                possible_moves.append(self.contains_piece.move_queen()[3])
                possible_moves.append(self.contains_piece.move_queen()[4])
                possible_moves.append(self.contains_piece.move_queen()[5])
                possible_moves.append(self.contains_piece.move_queen()[6])
                possible_moves.append(self.contains_piece.move_queen()[7])
            elif self.contains_piece.get_piece_name() == 'king':
                possible_moves.append(self.contains_piece.move_king()[0])
                possible_moves.append(self.contains_piece.move_king()[1])
            return possible_moves
