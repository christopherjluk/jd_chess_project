# Chessboard class for the chess game

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QPushButton,
)
from PyQt5.QtGui import QFont

from Components.square import Square
from Components.chesspiece import Chesspiece


class Chessboard(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.exchange_widget = QWidget()
        self.game_running = True
        self.initial_setup = True
        self.turn_white = False
        self.turn_color = 'white'
        self.other_color = 'black'
        self.last_moved_piece = None
        self.last_move = []
        self.setWindowTitle("Chessboard")
        self.board_layout = QGridLayout()
        self.passant_flag = False
        self.castling_flag = False
        self.white_king_location = []
        self.black_king_location = []
        self.connect_list = []
        self.squares = [[], [], [], [], [], [], [], []]
        self.setup_chessboard()
        self.setup_pieces()
        
        self.setLayout(self.board_layout)
        self.setFixedHeight(500)
        self.setFixedWidth(500)
        self.exchange_widget.setVisible(False)

    def setup_chessboard(self):
        """
        Function for setting up the chessboard
        """
        horizontal_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        vertical_labels = ['1', '2', '3', '4', '5', '6', '7', '8']
        for i in range(8): # Iterate through columns
            self.board_layout.addWidget(QLabel(horizontal_labels[i]), 0, i + 1, 1, 1)
            for j in range(8): # Iterate through rows
                self.board_layout.addWidget(QLabel(vertical_labels[j]), 8 - j, 0, 1, 1)
                if((i + j) % 2 == 0):
                    self.squares[i].append(Square("green", i, j))
                else:
                    self.squares[i].append(Square("gold", i, j))
                self.board_layout.addWidget(self.squares[i][j], 8 - j, i + 1, 1, 1)


    def setup_pieces(self):
        """
        Function for setting the pieces up on the board
        """
        for i in range(8):
            for j in range(8):
                if(self.squares[i][j].has_piece()):
                    if(self.squares[i][j].contains_piece.get_piece_color() == self.turn_color):
                        if not self.initial_setup:
                            self.squares[i][j].disconnect()
                        self.squares[i][j].setCheckable(False)

        for i in range(8):
            for j in range(8):
                self.squares[i][j].setup_piece(None)

        self.white_king_location.clear()
        self.black_king_location.clear()

        # White Pawns
        self.squares[0][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[1][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[2][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[3][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[4][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[5][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[6][1].setup_piece(Chesspiece('white', 'pawn'))
        self.squares[7][1].setup_piece(Chesspiece('white', 'pawn'))

        # White Rooks
        self.squares[0][0].setup_piece(Chesspiece('white', 'rook'))
        self.squares[7][0].setup_piece(Chesspiece('white', 'rook'))

        # White Knights
        self.squares[1][0].setup_piece(Chesspiece('white', 'knight'))
        self.squares[6][0].setup_piece(Chesspiece('white', 'knight'))

        # White Bishops
        self.squares[2][0].setup_piece(Chesspiece('white', 'bishop'))
        self.squares[5][0].setup_piece(Chesspiece('white', 'bishop'))

        # White Royalty
        self.squares[3][0].setup_piece(Chesspiece('white', 'queen'))
        self.squares[4][0].setup_piece(Chesspiece('white', 'king'))
        self.white_king_location.append(4)
        self.white_king_location.append(0)

        # Black Pawns
        self.squares[0][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[1][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[2][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[3][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[4][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[5][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[6][6].setup_piece(Chesspiece('black', 'pawn'))
        self.squares[7][6].setup_piece(Chesspiece('black', 'pawn'))

        # Black Rooks
        self.squares[0][7].setup_piece(Chesspiece('black', 'rook'))
        self.squares[7][7].setup_piece(Chesspiece('black', 'rook'))

        # Black Knights
        self.squares[1][7].setup_piece(Chesspiece('black', 'knight'))
        self.squares[6][7].setup_piece(Chesspiece('black', 'knight'))

        # Black Bishops
        self.squares[2][7].setup_piece(Chesspiece('black', 'bishop'))
        self.squares[5][7].setup_piece(Chesspiece('black', 'bishop'))

        # Black Royalty
        self.squares[3][7].setup_piece(Chesspiece('black', 'queen'))
        self.squares[4][7].setup_piece(Chesspiece('black', 'king'))
        self.black_king_location.append(4)
        self.black_king_location.append(7)
        
        self.initial_setup = False
        self.turn_color = 'white'
        self.other_color = 'black'
        self.turn_white = True
        for i in range(8):
            for j in range(8):
                if(self.squares[i][j].has_piece()):
                    if(self.squares[i][j].contains_piece.get_piece_color() == self.turn_color):
                        value = True
                        self.squares[i][j].clicked.connect(lambda value, i=i, j=j: self.button_checked(i, j))
                        self.squares[i][j].setCheckable(True)

    def possible_moves(self, color):
        """
        Function for checking the amount of possible moves

        Inputs
            color : str
                The color that is being checked
        Outputs
            num_moves : int
                The number of moves a color has
        """
        num_moves = 0
        origin_list = []
        moves_list = []
        for col in range(8):
            for row in range(8):
                condition_has_piece = self.squares[col][row].has_piece()
                if condition_has_piece:
                    condition_right_color = (self.squares[col][row].contains_piece.get_piece_color() == color)
                else:
                    condition_right_color = False
                if(condition_has_piece and condition_right_color):
                    possible_moves = self.squares[col][row].move_piece()
                    part = self.squares[col][row].contains_piece.get_piece_name()
                    if(part == 'knight'):
                        for move in possible_moves:
                            if(not self.squares[move[0]][move[1]].has_piece()):
                                num_moves = num_moves + 1
                                moves_list.append(self.squares[move[0]][move[1]])
                                origin_list.append(self.squares[col][row])
                            elif(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                                num_moves = num_moves + 1
                                moves_list.append(self.squares[move[0]][move[1]])
                                origin_list.append(self.squares[col][row])
                    elif(part == 'king'):
                        for condition in possible_moves:
                            for move in condition:
                                if(condition == possible_moves[0]):
                                    if(not self.squares[move[0]][move[1]].has_piece()):
                                        num_moves = num_moves + 1
                                        moves_list.append(self.squares[move[0]][move[1]])
                                        origin_list.append(self.squares[col][row])
                                    elif(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                                        num_moves = num_moves + 1
                                        moves_list.append(self.squares[move[0]][move[1]])
                                        origin_list.append(self.squares[col][row])
                                else:
                                    if(move == condition[0]):
                                        condition1_1 = not self.squares[move[0]][move[1]].has_piece()
                                        condition1_2 = not self.squares[move[0] - 1][move[1]].has_piece()
                                        condition1 = condition1_1 and condition1_2
                                        if color == 'white' and self.squares[7][0].has_piece():
                                            condition2 = (self.squares[7][0].contains_piece.get_piece_name() == 'rook')
                                            condition3 = (self.squares[7][0].contains_piece.moved == 0)
                                            condition4 = not self.in_check(self.white_king_location[0], self.white_king_location[1])
                                            condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                            condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col - 1, self.squares[move[0]][move[1]].row)
                                            condition5 = condition5_1 and condition5_2
                                        elif color == 'black' and self.squares[7][7].has_piece():
                                            condition2 = (self.squares[7][7].contains_piece.get_piece_name() == 'rook')
                                            condition3 = (self.squares[7][7].contains_piece.moved == 0)
                                            condition4 = not self.in_check(self.black_king_location[0], self.black_king_location[1])
                                            condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                            condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col + 1, self.squares[move[0]][move[1]].row)
                                            condition5 = condition5_1 and condition5_2
                                        else:
                                            condition2 = False
                                            condition3 = False
                                            condition4 = False
                                            condition5 = False
                                    else:
                                        condition1_1 = not self.squares[move[0]][move[1]].has_piece()
                                        condition1_2 = not self.squares[move[0] + 1][move[1]].has_piece()
                                        condition1_3 = not self.squares[move[0] - 1][move[1]].has_piece()
                                        condition1 = condition1_1 and condition1_2 and condition1_3
                                        if color == 'white' and self.squares[0][0].has_piece():
                                            condition2 = (self.squares[0][0].contains_piece.get_piece_name() == 'rook')
                                            condition3 = (self.squares[0][0].contains_piece.moved == 0)
                                            condition4 = not self.in_check(self.white_king_location[0], self.white_king_location[1])
                                            condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                            condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col - 1, self.squares[move[0]][move[1]].row)
                                            condition5 = condition5_1 and condition5_2
                                        elif color == 'black' and self.squares[0][7].has_piece():
                                            condition2 = (self.squares[0][7].contains_piece.get_piece_name() == 'rook')
                                            condition3 = (self.squares[0][7].contains_piece.moved == 0)
                                            condition4 = not self.in_check(self.black_king_location[0], self.black_king_location[1])
                                            condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                            condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col + 1, self.squares[move[0]][move[1]].row)
                                            condition5 = condition5_1 and condition5_2
                                        else:
                                            condition2 = False
                                            condition3 = False
                                            condition4 = False
                                            condition5 = False
                                    if(condition1 and condition2 and condition3 and condition4 and condition5):
                                        num_moves = num_moves + 1
                                        moves_list.append(self.squares[move[0]][move[1]])
                                        origin_list.append(self.squares[col][row])
                    elif(part == 'pawn'):
                        for condition in possible_moves:
                            if(condition == possible_moves[0]):
                                for move in condition:
                                    if(not self.squares[move[0]][move[1]].has_piece()):
                                        num_moves = num_moves + 1
                                        moves_list.append(self.squares[move[0]][move[1]])
                                        origin_list.append(self.squares[col][row])
                                    else:
                                        break
                            elif(condition == possible_moves[1]):
                                for move in condition:
                                    condition_1 = self.squares[move[0]][move[1]].has_piece()
                                    condition_2 = self.last_moved_piece == 'pawn'
                                    if len(self.last_move) > 0:
                                        condition_3 = (self.last_move[0] == self.squares[col][row].col + 1) or (self.last_move[0] == self.squares[col][row].col - 1)
                                    else:
                                        condition_3 = False
                                    condition_4 = (self.other_color == 'black' and self.squares[col][row].row == 4) or (self.other_color == 'white' and self.squares[col][row].row == 3)
                                    if(condition_1):
                                        if(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                                            num_moves = num_moves + 1
                                            moves_list.append(self.squares[move[0]][move[1]])
                                            origin_list.append(self.squares[col][row])
                                    elif(condition_2 and condition_3 and condition_4):
                                        if(self.other_color == 'black' and self.squares[move[0]][move[1] - 1].has_piece()):
                                            if(self.squares[move[0]][move[1] - 1].contains_piece.get_piece_color() == 'black'):
                                                if((self.last_move[0] == self.squares[move[0]][move[1]].col) and self.last_move[1] == (self.squares[move[0]][move[1]].row - 1)):
                                                    num_moves = num_moves + 1
                                                    moves_list.append(self.squares[move[0]][move[1]])
                                                    origin_list.append(self.squares[col][row])
                                        elif(self.other_color == 'white' and self.squares[move[0]][move[1] + 1].has_piece()):
                                            if(self.squares[move[0]][move[1] + 1].contains_piece.get_piece_color() == 'white'):
                                                if((self.last_move[0] == self.squares[move[0]][move[1]].col) and self.last_move[1] == (self.squares[move[0]][move[1]].row + 1)):
                                                    num_moves = num_moves + 1
                                                    moves_list.append(self.squares[move[0]][move[1]])
                                                    origin_list.append(self.squares[col][row])
                    else:
                        for direction in possible_moves:
                            for move in direction:
                                if(not self.squares[move[0]][move[1]].has_piece()):
                                    num_moves = num_moves + 1
                                    moves_list.append(self.squares[move[0]][move[1]])
                                    origin_list.append(self.squares[col][row])
                                elif(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                                    num_moves = num_moves + 1
                                    moves_list.append(self.squares[move[0]][move[1]])
                                    origin_list.append(self.squares[col][row])
                                    break
                                else:
                                    break
        remove_flag = False
        iter = 0
        while iter < len(moves_list):
            remove_flag = False
            if(origin_list[iter].contains_piece.get_piece_name() == 'king'):
                old_piece = None
                if(self.squares[moves_list[iter].col][moves_list[iter].row].has_piece()):
                    old_piece = self.squares[moves_list[iter].col][moves_list[iter].row].contains_piece
                self.squares[moves_list[iter].col][moves_list[iter].row].setup_piece(self.squares[origin_list[iter].col][origin_list[iter].row].get_piece())
                if self.in_check(moves_list[iter].col, moves_list[iter].row):
                    remove_flag = True
                self.squares[origin_list[iter].col][origin_list[iter].row].setup_piece(self.squares[moves_list[iter].col][moves_list[iter].row].get_piece())
                self.squares[moves_list[iter].col][moves_list[iter].row].setup_piece(old_piece)
            else:
                old_piece = None
                if(self.squares[moves_list[iter].col][moves_list[iter].row].has_piece()):
                    old_piece = self.squares[moves_list[iter].col][moves_list[iter].row].contains_piece
                self.squares[moves_list[iter].col][moves_list[iter].row].setup_piece(self.squares[origin_list[iter].col][origin_list[iter].row].get_piece())
                self.squares[origin_list[iter].col][origin_list[iter].row].setup_piece(None)
                if color == 'white':
                    if self.in_check(self.white_king_location[0], self.white_king_location[1]):
                        remove_flag = True
                else:
                    if self.in_check(self.black_king_location[0], self.black_king_location[1]):
                        remove_flag = True
                self.squares[origin_list[iter].col][origin_list[iter].row].setup_piece(self.squares[moves_list[iter].col][moves_list[iter].row].get_piece())
                self.squares[moves_list[iter].col][moves_list[iter].row].setup_piece(old_piece)
            if remove_flag:
                index = moves_list.index(self.squares[moves_list[iter].col][moves_list[iter].row])
                del moves_list[index]
                del origin_list[index]
                iter = iter - 1
                num_moves = num_moves - 1
            iter = iter + 1
        return num_moves

    def button_checked(self, col : int, row : int):
        """
        Function for unchecking every other button and showing possible moves
        
        Inputs
            col : int
                The columm of the clicked button
            row : int
                The row of the clicked button
        """
        for square in self.connect_list:
            square.disconnect()
            if(not square.has_piece()):
                square.setCheckable(False)
            square.reset_color()
        self.connect_list.clear()
        self.passant_flag = False
        self.castling_flag = False

        for i in range(8):
            for j in range(8):
                if not (i == col and j == row):
                    self.squares[i][j].setChecked(False)
        
        if self.turn_white:
            if self.in_check(self.white_king_location[0], self.white_king_location[1]):
                self.squares[self.white_king_location[0]][self.white_king_location[1]].setStyleSheet("background-color : red")
        else:
            if self.in_check(self.black_king_location[0], self.black_king_location[1]):
                self.squares[self.black_king_location[0]][self.black_king_location[1]].setStyleSheet("background-color : red")

        if(self.squares[col][row].isChecked()):
            possible_moves = self.squares[col][row].move_piece()
            part = self.squares[col][row].contains_piece.get_piece_name()
            if(part == 'knight'):
                self.passant_flag = False
                self.castling_flag = False
                for move in possible_moves:
                    if(not self.squares[move[0]][move[1]].has_piece()):
                        self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                        self.squares[move[0]][move[1]].setCheckable(True)
                        self.connect_list.append(self.squares[move[0]][move[1]])
                    elif(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                        self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                        self.squares[move[0]][move[1]].setCheckable(True)
                        self.connect_list.append(self.squares[move[0]][move[1]])
            elif(part == 'king'):
                self.passant_flag = False
                for condition in possible_moves:
                    for move in condition:
                        if(condition == possible_moves[0]):
                            if(not self.squares[move[0]][move[1]].has_piece()):
                                self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                self.squares[move[0]][move[1]].setCheckable(True)
                                self.connect_list.append(self.squares[move[0]][move[1]])
                            elif(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                                self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                self.squares[move[0]][move[1]].setCheckable(True)
                                self.connect_list.append(self.squares[move[0]][move[1]])
                        else:
                            if(move == condition[0]):
                                condition1_1 = not self.squares[move[0]][move[1]].has_piece()
                                condition1_2 = not self.squares[move[0] - 1][move[1]].has_piece()
                                condition1 = condition1_1 and condition1_2
                                if self.turn_white and self.squares[7][0].has_piece():
                                    condition2 = (self.squares[7][0].contains_piece.get_piece_name() == 'rook')
                                    condition3 = (self.squares[7][0].contains_piece.moved == 0)
                                    condition4 = not self.in_check(self.white_king_location[0], self.white_king_location[1])
                                    condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                    condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col - 1, self.squares[move[0]][move[1]].row)
                                    condition5 = condition5_1 and condition5_2
                                elif not self.turn_white and self.squares[7][7].has_piece():
                                    condition2 = (self.squares[7][7].contains_piece.get_piece_name() == 'rook')
                                    condition3 = (self.squares[7][7].contains_piece.moved == 0)
                                    condition4 = not self.in_check(self.black_king_location[0], self.black_king_location[1])
                                    condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                    condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col + 1, self.squares[move[0]][move[1]].row)
                                    condition5 = condition5_1 and condition5_2
                                else:
                                    condition2 = False
                                    condition3 = False
                                    condition4 = False
                                    condition5 = False
                            else:
                                condition1_1 = not self.squares[move[0]][move[1]].has_piece()
                                condition1_2 = not self.squares[move[0] + 1][move[1]].has_piece()
                                condition1_3 = not self.squares[move[0] - 1][move[1]].has_piece()
                                condition1 = condition1_1 and condition1_2 and condition1_3
                                if self.turn_white and self.squares[0][0].has_piece():
                                    condition2 = (self.squares[0][0].contains_piece.get_piece_name() == 'rook')
                                    condition3 = (self.squares[0][0].contains_piece.moved == 0)
                                    condition4 = not self.in_check(self.white_king_location[0], self.white_king_location[1])
                                    condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                    condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col - 1, self.squares[move[0]][move[1]].row)
                                    condition5 = condition5_1 and condition5_2
                                elif not self.turn_white and self.squares[0][7].has_piece():
                                    condition2 = (self.squares[0][7].contains_piece.get_piece_name() == 'rook')
                                    condition3 = (self.squares[0][7].contains_piece.moved == 0)
                                    condition4 = not self.in_check(self.black_king_location[0], self.black_king_location[1])
                                    condition5_1 = not self.in_check(self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row)
                                    condition5_2 = not self.in_check(self.squares[move[0]][move[1]].col + 1, self.squares[move[0]][move[1]].row)
                                    condition5 = condition5_1 and condition5_2
                                else:
                                    condition2 = False
                                    condition3 = False
                                    condition4 = False
                                    condition5 = False
                            if(condition1 and condition2 and condition3 and condition4 and condition5):
                                self.castling_flag = True
                                self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                self.squares[move[0]][move[1]].setCheckable(True)
                                self.connect_list.append(self.squares[move[0]][move[1]])
            elif(part == 'pawn'):
                self.castling_flag = False
                for condition in possible_moves:
                    if(condition == possible_moves[0]):
                        for move in condition:
                            if(not self.squares[move[0]][move[1]].has_piece()):
                                self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                self.squares[move[0]][move[1]].setCheckable(True)
                                self.connect_list.append(self.squares[move[0]][move[1]])
                            else:
                                break
                    elif(condition == possible_moves[1]):
                        for move in condition:
                            condition_1 = self.squares[move[0]][move[1]].has_piece()
                            condition_2 = self.last_moved_piece == 'pawn'
                            if len(self.last_move) > 0:
                                condition_3 = (self.last_move[0] == self.squares[col][row].col + 1) or (self.last_move[0] == self.squares[col][row].col - 1)
                            else:
                                condition_3 = False
                            condition_4 = (self.other_color == 'black' and self.squares[col][row].row == 4) or (self.other_color == 'white' and self.squares[col][row].row == 3)
                            if(condition_1):
                                if(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                                    self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                    self.squares[move[0]][move[1]].setCheckable(True)
                                    self.connect_list.append(self.squares[move[0]][move[1]])
                            elif(condition_2 and condition_3 and condition_4):
                                self.passant_flag = True
                                if(self.other_color == 'black' and self.squares[move[0]][move[1] - 1].has_piece()):
                                    if(self.squares[move[0]][move[1] - 1].contains_piece.get_piece_color() == 'black'):
                                        if((self.last_move[0] == self.squares[move[0]][move[1]].col) and self.last_move[1] == (self.squares[move[0]][move[1]].row - 1)):
                                            self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                            self.squares[move[0]][move[1]].setCheckable(True)
                                            self.connect_list.append(self.squares[move[0]][move[1]])
                                elif(self.other_color == 'white' and self.squares[move[0]][move[1] + 1].has_piece()):
                                    if(self.squares[move[0]][move[1] + 1].contains_piece.get_piece_color() == 'white'):
                                        if((self.last_move[0] == self.squares[move[0]][move[1]].col) and self.last_move[1] == (self.squares[move[0]][move[1]].row + 1)):
                                            self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                                            self.squares[move[0]][move[1]].setCheckable(True)
                                            self.connect_list.append(self.squares[move[0]][move[1]])
            else:
                self.passant_flag = False
                self.castling_flag = False
                for direction in possible_moves:
                    for move in direction:
                        if(not self.squares[move[0]][move[1]].has_piece()):
                            self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                            self.squares[move[0]][move[1]].setCheckable(True)
                            self.connect_list.append(self.squares[move[0]][move[1]])
                        elif(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.other_color):
                            self.squares[move[0]][move[1]].setStyleSheet("background-color : lightblue")
                            self.squares[move[0]][move[1]].setCheckable(True)
                            self.connect_list.append(self.squares[move[0]][move[1]])
                            break
                        else:
                            break
            iter = 0
            while iter < len(self.connect_list):
                remove_flag = False
                if(part == 'king'):
                    old_piece = None
                    if(self.squares[self.connect_list[iter].col][self.connect_list[iter].row].has_piece()):
                        old_piece = self.squares[self.connect_list[iter].col][self.connect_list[iter].row].contains_piece
                    self.squares[self.connect_list[iter].col][self.connect_list[iter].row].setup_piece(self.squares[col][row].get_piece())
                    if self.in_check(self.connect_list[iter].col, self.connect_list[iter].row):
                        remove_flag = True
                    self.squares[col][row].setup_piece(self.squares[self.connect_list[iter].col][self.connect_list[iter].row].get_piece())
                    self.squares[self.connect_list[iter].col][self.connect_list[iter].row].setup_piece(old_piece)
                else:
                    old_piece = None
                    if(self.squares[self.connect_list[iter].col][self.connect_list[iter].row].has_piece()):
                        old_piece = self.squares[self.connect_list[iter].col][self.connect_list[iter].row].contains_piece
                    self.squares[self.connect_list[iter].col][self.connect_list[iter].row].setup_piece(self.squares[col][row].get_piece())
                    self.squares[col][row].setup_piece(None)
                    if self.turn_white:
                        if self.in_check(self.white_king_location[0], self.white_king_location[1]):
                            remove_flag = True
                    else:
                        if self.in_check(self.black_king_location[0], self.black_king_location[1]):
                            remove_flag = True
                    self.squares[col][row].setup_piece(self.squares[self.connect_list[iter].col][self.connect_list[iter].row].get_piece())
                    self.squares[self.connect_list[iter].col][self.connect_list[iter].row].setup_piece(old_piece)
                if remove_flag:
                    self.squares[self.connect_list[iter].col][self.connect_list[iter].row].setCheckable(False)
                    self.squares[self.connect_list[iter].col][self.connect_list[iter].row].reset_color()
                    self.connect_list.remove(self.squares[self.connect_list[iter].col][self.connect_list[iter].row])
                    iter = iter - 1
                iter = iter + 1
            for square in self.connect_list:
                value = True
                square.clicked.connect(lambda value, col=col, row=row, square=square: self.piece_moved(col, row, square))

    def piece_moved(self, col : int, row : int, square : Square):
        """
        Function for moving a piece

        Inputs
            col : int
                The old chesspiece column
            row : int
                The old chesspiece row
            square : square
                The new place where the chesspiece is being moved
        """
        for i in range(8):
            for j in range(8):
                self.squares[i][j].reset_color()

        old_piece = None
        self.last_move.clear()
        if self.squares[square.col][square.row].has_piece():
            old_piece = self.squares[square.col][square.row].contains_piece.get_piece_name()
        self.squares[square.col][square.row].setup_piece(self.squares[col][row].get_piece())
        if self.squares[square.col][square.row].has_piece():
            self.squares[square.col][square.row].contains_piece.moved = self.squares[square.col][square.row].contains_piece.moved + 1
            self.last_moved_piece = self.squares[square.col][square.row].contains_piece.get_piece_name()
            self.last_move.append(square.col)
            self.last_move.append(square.row)
        if self.passant_flag:
            if self.turn_white:
                self.squares[square.col][square.row - 1].setup_piece(None)
            else:
                self.squares[square.col][square.row + 1].setup_piece(None)

        if self.last_moved_piece == 'king':
            if self.turn_white:
                self.white_king_location.clear()
                self.white_king_location.append(square.col)
                self.white_king_location.append(square.row)
            else:
                self.black_king_location.clear()
                self.black_king_location.append(square.col)
                self.black_king_location.append(square.row)

        if (col + row) % 2 == 0:
            new_square = Square("green", col, row)
        else:
            new_square = Square("gold", col, row)

        new_col = square.col
        new_row = square.row

        for dissquare in self.connect_list:
            dissquare.disconnect()
            if(not dissquare.has_piece()):
                dissquare.setCheckable(False)
            dissquare.reset_color()
        self.connect_list.clear()
        
        if self.castling_flag:
            if self.turn_white:
                if self.squares[square.col][square.row].col == 6:
                    self.squares[5][0].setup_piece(self.squares[7][0].get_piece())
                    self.squares[7][0].disconnect()
                    self.squares[5][0].clicked.connect(lambda: self.button_checked(5, 0))
                    self.board_layout.removeWidget(self.squares[7][0])
                    self.squares[7][0] = Square("gold", 7, 0)
                    self.board_layout.addWidget(self.squares[7][0], 8, 8, 1, 1)
                    self.squares[7][0].setChecked(False)
                else:
                    self.squares[3][0].setup_piece(self.squares[0][0].get_piece())
                    self.squares[0][0].disconnect()
                    self.squares[3][0].clicked.connect(lambda: self.button_checked(3, 0))
                    self.board_layout.removeWidget(self.squares[0][0])
                    self.squares[0][0] = Square("green", 0, 0)
                    self.board_layout.addWidget(self.squares[0][0], 8, 1, 1, 1)
                    self.squares[0][0].setChecked(False)
            else:
                if self.squares[square.col][square.row].col == 6:
                    self.squares[5][7].setup_piece(self.squares[7][7].get_piece())
                    self.squares[7][7].disconnect()
                    self.squares[5][7].clicked.connect(lambda: self.button_checked(5, 7))
                    self.board_layout.removeWidget(self.squares[7][7])
                    self.squares[7][7] = Square("green", 7, 7)
                    self.board_layout.addWidget(self.squares[7][7], 1, 8, 1, 1)
                    self.squares[7][7].setChecked(False)
                else:
                    self.squares[3][7].setup_piece(self.squares[0][7].get_piece())
                    self.squares[0][7].disconnect()
                    self.squares[3][7].clicked.connect(lambda: self.button_checked(3, 7))
                    self.board_layout.removeWidget(self.squares[0][7])
                    self.squares[0][7] = Square("gold", 0, 7)
                    self.board_layout.addWidget(self.squares[0][7], 1, 1, 1, 1)
                    self.squares[0][7].setChecked(False)
        
        self.squares[col][row].disconnect()
        self.board_layout.removeWidget(self.squares[col][row])
        self.squares[col][row] = new_square
        self.board_layout.addWidget(self.squares[col][row], 8 - row, 1 + col, 1, 1)
        self.squares[new_col][new_row].setChecked(False)
        self.squares[new_col][new_row].clicked.connect(lambda : self.button_checked(new_col, new_row))

        if old_piece == 'king':
            self.game_running = False

        if self.squares[new_col][new_row].contains_piece.get_piece_name() == 'pawn':
            if(self.squares[new_col][new_row].contains_piece.get_piece_color() == 'white' and new_row == 7):
                if self.exchange_widget.layout() is not None:
                    QWidget().setLayout(self.exchange_widget.layout())
                white_exchange_layout = QGridLayout()
                white_exchange_layout.addWidget(QLabel("Choose a piece to exchange"), 0, 0, 1, 4)
                button_1 = QPushButton('♕')
                button_1.setFont(QFont('Times', 28))
                button_1.setFixedHeight(50)
                button_1.setFixedWidth(50)
                button_2 = QPushButton('♘')
                button_2.setFont(QFont('Times', 28))
                button_2.setFixedHeight(50)
                button_2.setFixedWidth(50)
                button_3 = QPushButton('♗')
                button_3.setFont(QFont('Times', 28))
                button_3.setFixedHeight(50)
                button_3.setFixedWidth(50)
                button_4 = QPushButton('♖')
                button_4.setFont(QFont('Times', 28))
                button_4.setFixedHeight(50)
                button_4.setFixedWidth(50)
                value = True
                button_1.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 1))
                button_2.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 2))
                button_3.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 3))
                button_4.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 4))
                white_exchange_layout.addWidget(button_1, 1, 0, 1, 1)
                white_exchange_layout.addWidget(button_2, 1, 1, 1, 1)
                white_exchange_layout.addWidget(button_3, 1, 2, 1, 1)
                white_exchange_layout.addWidget(button_4, 1, 3, 1, 1)
                self.exchange_widget.setLayout(white_exchange_layout)
                if self.game_running:
                    self.exchange_widget.setVisible(True)
            elif(self.squares[new_col][new_row].contains_piece.get_piece_color() == 'black' and new_row == 0):
                if self.exchange_widget.layout() is not None:
                    QWidget().setLayout(self.exchange_widget.layout())
                black_exchange_layout = QGridLayout()
                black_exchange_layout.addWidget(QLabel("Choose a piece to exchange"), 0, 0, 1, 4)
                button_1 = QPushButton('♛')
                button_1.setFont(QFont('Times', 28))
                button_1.setFixedHeight(50)
                button_1.setFixedWidth(50)
                button_2 = QPushButton('♞')
                button_2.setFont(QFont('Times', 28))
                button_2.setFixedHeight(50)
                button_2.setFixedWidth(50)
                button_3 = QPushButton('♝')
                button_3.setFont(QFont('Times', 28))
                button_3.setFixedHeight(50)
                button_3.setFixedWidth(50)
                button_4 = QPushButton('♜')
                button_4.setFont(QFont('Times', 28))
                button_4.setFixedHeight(50)
                button_4.setFixedWidth(50)
                value = True
                button_1.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 1))
                button_2.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 2))
                button_3.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 3))
                button_4.clicked.connect(lambda value, col=new_col, row=new_row: self.pawn_exchange(col, row, 4))
                black_exchange_layout.addWidget(button_1, 1, 0, 1, 1)
                black_exchange_layout.addWidget(button_2, 1, 1, 1, 1)
                black_exchange_layout.addWidget(button_3, 1, 2, 1, 1)
                black_exchange_layout.addWidget(button_4, 1, 3, 1, 1)
                self.exchange_widget.setLayout(black_exchange_layout)
                if self.game_running:
                    self.exchange_widget.setVisible(True)
            else:
                self.change_turns()
        else:
            self.change_turns()

        if self.possible_moves(self.turn_color) == 0:
            if self.turn_white:
                if self.in_check(self.white_king_location[0], self.white_king_location[1]):
                    self.end_game(True)
                else:
                    self.end_game(False)
            else:
                if self.in_check(self.black_king_location[0], self.black_king_location[1]):
                    self.end_game(True)
                else:
                    self.end_game(False)

    def in_check(self, col_to_check, row_to_check):
        """
        Function for checking whether the king is in check
        
        Inputs
            col_to_check : int
                The column that the king is on or will be on
            row_to_check : int
                The row that the king is on or will be on

        Outputs
            check_flag : bool
                Whether the king is in check
        """
        check_flag = False
        check_list = []
        for i in range(8):
            for j in range(8):
                if(self.squares[i][j].has_piece()):
                    if(self.squares[i][j].contains_piece.get_piece_color() == self.other_color):
                        possible_moves = self.squares[i][j].move_piece()
                        part = self.squares[i][j].contains_piece.get_piece_name()
                        if(part == 'knight'):
                            for move in possible_moves:
                                if(self.squares[move[0]][move[1]].has_piece()):
                                    if(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.turn_color):
                                        check_list.append([self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row])
                        elif(part == 'king'):
                            for move in possible_moves[0]:
                                if(self.squares[move[0]][move[1]].has_piece()):
                                    if(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.turn_color):
                                        check_list.append([self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row])
                        elif(part == 'pawn'):
                            for condition in possible_moves:
                                if(condition == possible_moves[1]):
                                    for move in condition:
                                        if(self.squares[move[0]][move[1]].has_piece()):
                                            if(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.turn_color):
                                                check_list.append([self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row])
                        else:
                            for direction in possible_moves:
                                for move in direction:
                                    if(self.squares[move[0]][move[1]].has_piece()):
                                        if(self.squares[move[0]][move[1]].contains_piece.get_piece_color() == self.turn_color):
                                            check_list.append([self.squares[move[0]][move[1]].col, self.squares[move[0]][move[1]].row])
                                            break
        for move in check_list:
            if ((move[0] == col_to_check) and (move[1] == row_to_check)):
                check_flag = True
        return check_flag

    def end_game(self, winner: bool):
        """
        Function for ending the game

        Inputs
            winner : bool
                Whether there is a winner
        """
        for i in range(8):
            for j in range(8):
                self.squares[i][j].setCheckable(False)
        self.game_over_widget = QWidget()
        game_over_layout = QGridLayout()
        if winner:
            game_over_layout.addWidget(QLabel("Game Over: " + str(self.other_color) + " wins"), 0, 0, 1, 1)
        else:
            game_over_layout.addWidget(QLabel("Stalemate - Tie game"), 0, 0, 1, 1)
        self.game_over_widget.setLayout(game_over_layout)
        self.game_over_widget.setVisible(True)

    def change_turns(self):
        """
        Function for changing turns
        """
        self.other_color = self.turn_color
        self.turn_white = not self.turn_white
        if self.turn_white:
            self.turn_color = 'white'
        else:
            self.turn_color = 'black'
        for i in range(8):
            for j in range(8):
                if(self.squares[i][j].has_piece()):
                    if(self.squares[i][j].contains_piece.get_piece_color() == self.other_color):
                        self.squares[i][j].disconnect()
                        self.squares[i][j].setCheckable(False)
        for i in range(8):
            for j in range(8):
                if(self.squares[i][j].has_piece()):
                    if(self.squares[i][j].contains_piece.get_piece_color() == self.turn_color):
                        value = True
                        self.squares[i][j].clicked.connect(lambda value, i=i, j=j: self.button_checked(i, j))
                        self.squares[i][j].setCheckable(True)
        if self.turn_white:
            if self.in_check(self.white_king_location[0], self.white_king_location[1]):
                self.squares[self.white_king_location[0]][self.white_king_location[1]].setStyleSheet("background-color : red")
        else:
            if self.in_check(self.black_king_location[0], self.black_king_location[1]):
                self.squares[self.black_king_location[0]][self.black_king_location[1]].setStyleSheet("background-color : red")

    def pawn_exchange(self, col, row, option):
        """
        Function for exchanging a pawn

        Inputs
            col : int
                The current column of the piece
            row : int
                The current row of the piece
            option : int
                The option user chose to exchange
        """
        if self.game_running:
            num_moves = self.squares[col][row].contains_piece.moved
            if (col + row) % 2 == 0:
                new_square = Square("green", col, row)
            else:
                new_square = Square("gold", col, row)
            self.board_layout.removeWidget(self.squares[col][row])
            self.squares[col][row] = new_square
            self.board_layout.addWidget(self.squares[col][row], 8 - row, col + 1, 1, 1)
            self.squares[col][row].setChecked(False)
            self.squares[col][row].clicked.connect(lambda : self.button_checked(col, row))
            if option == 1:
                self.squares[col][row].setup_piece(Chesspiece(self.turn_color, 'queen'))
            elif option == 2:
                self.squares[col][row].setup_piece(Chesspiece(self.turn_color, 'knight'))
            elif option == 3:
                self.squares[col][row].setup_piece(Chesspiece(self.turn_color, 'bishop'))
            elif option == 4:
                self.squares[col][row].setup_piece(Chesspiece(self.turn_color, 'rook'))
            self.squares[col][row].contains_piece.moved = num_moves
            self.squares[col][row].setCheckable(False)
            self.change_turns()
            self.exchange_widget.setVisible(False)
