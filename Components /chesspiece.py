# Chesspiece class for the board game


class Chesspiece(object):
    def __init__(self, color = 'white', type = None):
        self.color = color
        self.type = type
        self.position = [-1, -1]
        self.moved = 0

    def set_position(self, col : int, row : int):
        """
        Function for setting the position of the piece

        Inputs
            col : int
                The column of the current chesspiece
            row : int
                The row of the current chesspiece
        """
        self.position = [col, row]

    def get_position(self):
        """
        Function for returning the position of the piece

        Inputs
            self.position : list
                The current position of the chesspiece
        """

    def get_piece_color(self):
        """
        Function for returning the color of the piece

        Outputs
            self.color : str
                The color of the piece
        """
        return self.color

    def get_piece_name(self):
        """
        Function for returning the name of the piece

        Outputs
            self.type : str
                The type of piece
        """
        return self.type

    def get_pixel_image(self):
        """
        Function for returning the pixel image of the piece

        Outputs
            pixel_image : str
                The pixel image of the piece
        """
        if self.color == 'white':
            if self.type == 'pawn':
                return '♙'
            elif self.type == 'rook':
                return '♖'
            elif self.type == 'knight':
                return '♘'
            elif self.type == 'bishop':
                return '♗'
            elif self.type == 'queen':
                return '♕'
            elif self.type == 'king':
                return '♔'
        else:
            if self.type == 'pawn':
                return '♟'
            elif self.type == 'rook':
                return '♜'
            elif self.type == 'knight':
                return '♞'
            elif self.type == 'bishop':
                return '♝'
            elif self.type == 'queen':
                return '♛'
            elif self.type == 'king':
                return '♚'
            
    def move_pawn(self):
        possible_moves = []
        if self.color == 'white':
            possible_moves.append([])
            if self.position[1] <= 6:
                possible_moves[0].append([self.position[0], self.position[1] + 1])
            if self.moved == 0:
                possible_moves[0].append([self.position[0], self.position[1] + 2])
            possible_moves.append([])
            if self.position[1] <= 6:
                if self.position[0] - 1 >= 0:
                    possible_moves[1].append([self.position[0] - 1, self.position[1] + 1])
                if self.position[0] + 1 <= 7:
                    possible_moves[1].append([self.position[0] + 1, self.position[1] + 1])
        else:
            possible_moves.append([])
            if self.position[1] >= 1:
                possible_moves[0].append([self.position[0], self.position[1] - 1])
            if self.moved == 0:
                possible_moves[0].append([self.position[0], self.position[1] - 2])
            possible_moves.append([])
            if self.position[1] >= 1:
                if self.position[0] - 1 >= 0:
                    possible_moves[1].append([self.position[0] - 1, self.position[1] - 1])
                if self.position[0] + 1 <= 7:
                    possible_moves[1].append([self.position[0] + 1, self.position[1] - 1])
        return possible_moves
    
    def move_rook(self):
        possible_moves = []
        iter = self.position[0] + 1
        possible_moves.append([])
        while(iter <= 7):
            possible_moves[0].append([iter, self.position[1]])
            iter = iter + 1
        iter = self.position[0] - 1
        possible_moves.append([])
        while(iter >= 0):
            possible_moves[1].append([iter, self.position[1]])
            iter = iter - 1
        iter = self.position[1] + 1
        possible_moves.append([])
        while(iter <= 7):
            possible_moves[2].append([self.position[0], iter])
            iter = iter + 1
        iter = self.position[1] - 1
        possible_moves.append([])
        while(iter >= 0):
            possible_moves[3].append([self.position[0], iter])
            iter = iter - 1
        return possible_moves
    
    def move_knight(self):
        possible_moves = []
        condition0_1 = (self.position[0] - 2 >= 0)
        condition0_2 = (self.position[0] - 1 >= 0)
        condition0_3 = (self.position[0] + 1 <= 7)
        condition0_4 = (self.position[0] + 2 <= 7)
        condition1_1 = (self.position[1] - 2 >= 0)
        condition1_2 = (self.position[1] - 1 >= 0)
        condition1_3 = (self.position[1] + 1 <= 7)
        condition1_4 = (self.position[1] + 2 <= 7)
        if(condition0_1 and condition1_2):
            possible_moves.append([self.position[0] - 2, self.position[1] - 1])
        if(condition0_1 and condition1_3):
            possible_moves.append([self.position[0] - 2, self.position[1] + 1])
        if(condition0_2 and condition1_1):
            possible_moves.append([self.position[0] - 1, self.position[1] - 2])
        if(condition0_2 and condition1_4):
            possible_moves.append([self.position[0] - 1, self.position[1] + 2])
        if(condition0_3 and condition1_1):
            possible_moves.append([self.position[0] + 1, self.position[1] - 2])
        if(condition0_3 and condition1_4):
            possible_moves.append([self.position[0] + 1, self.position[1] + 2])
        if(condition0_4 and condition1_2):
            possible_moves.append([self.position[0] + 2, self.position[1] - 1])
        if(condition0_4 and condition1_3):
            possible_moves.append([self.position[0] + 2, self.position[1] + 1])
        return possible_moves
    
    def move_bishop(self):
        possible_moves = []
        iter1 = self.position[0] - 1
        iter2 = self.position[1] - 1
        possible_moves.append([])
        while(iter1 >= 0 and iter2 >= 0):
            possible_moves[0].append([iter1, iter2])
            iter1 = iter1 - 1
            iter2 = iter2 - 1
        iter1 = self.position[0] - 1
        iter2 = self.position[1] + 1
        possible_moves.append([])
        while(iter1 >= 0 and iter2 <= 7):
            possible_moves[1].append([iter1, iter2])
            iter1 = iter1 - 1
            iter2 = iter2 + 1
        iter1 = self.position[0] + 1
        iter2 = self.position[1] - 1
        possible_moves.append([])
        while(iter1 <= 7 and iter2 >= 0):
            possible_moves[2].append([iter1, iter2])
            iter1 = iter1 + 1
            iter2 = iter2 - 1
        iter1 = self.position[0] + 1
        iter2 = self.position[1] + 1
        possible_moves.append([])
        while(iter1 <= 7 and iter2 <= 7):
            possible_moves[3].append([iter1, iter2])
            iter1 = iter1 + 1
            iter2 = iter2 + 1
        return possible_moves
    
    def move_queen(self):
        possible_moves = []
        iter = self.position[0] + 1
        possible_moves.append([])
        while(iter <= 7):
            possible_moves[0].append([iter, self.position[1]])
            iter = iter + 1
        iter = self.position[0] - 1
        possible_moves.append([])
        while(iter >= 0):
            possible_moves[1].append([iter, self.position[1]])
            iter = iter - 1
        iter = self.position[1] + 1
        possible_moves.append([])
        while(iter <= 7):
            possible_moves[2].append([self.position[0], iter])
            iter = iter + 1
        iter = self.position[1] - 1
        possible_moves.append([])
        while(iter >= 0):
            possible_moves[3].append([self.position[0], iter])
            iter = iter - 1
        iter1 = self.position[0] - 1
        iter2 = self.position[1] - 1
        possible_moves.append([])
        while(iter1 >= 0 and iter2 >= 0):
            possible_moves[4].append([iter1, iter2])
            iter1 = iter1 - 1
            iter2 = iter2 - 1
        iter1 = self.position[0] - 1
        iter2 = self.position[1] + 1
        possible_moves.append([])
        while(iter1 >= 0 and iter2 <= 7):
            possible_moves[5].append([iter1, iter2])
            iter1 = iter1 - 1
            iter2 = iter2 + 1
        iter1 = self.position[0] + 1
        iter2 = self.position[1] - 1
        possible_moves.append([])
        while(iter1 <= 7 and iter2 >= 0):
            possible_moves[6].append([iter1, iter2])
            iter1 = iter1 + 1
            iter2 = iter2 - 1
        iter1 = self.position[0] + 1
        iter2 = self.position[1] + 1
        possible_moves.append([])
        while(iter1 <= 7 and iter2 <= 7):
            possible_moves[7].append([iter1, iter2])
            iter1 = iter1 + 1
            iter2 = iter2 + 1
        return possible_moves
        
    
    def move_king(self):
        possible_moves = []
        condition_1 = (self.position[0] - 1 >= 0)
        condition_2 = (self.position[0] + 1 <= 7)
        condition_3 = (self.position[1] - 1 >= 0)
        condition_4 = (self.position[1] + 1 <= 7)
        possible_moves.append([])
        if condition_1:
            possible_moves[0].append([self.position[0] - 1, self.position[1]])
        if condition_1 and condition_3:
            possible_moves[0].append([self.position[0] - 1, self.position[1] - 1])
        if condition_1 and condition_4:
            possible_moves[0].append([self.position[0] - 1, self.position[1] + 1])
        if condition_2:
            possible_moves[0].append([self.position[0] + 1, self.position[1]])
        if condition_2 and condition_3:
            possible_moves[0].append([self.position[0] + 1, self.position[1] - 1])
        if condition_2 and condition_4:
            possible_moves[0].append([self.position[0] + 1, self.position[1] + 1])
        if condition_3:
            possible_moves[0].append([self.position[0], self.position[1] - 1])
        if condition_4:
            possible_moves[0].append([self.position[0], self.position[1] + 1])
        possible_moves.append([])
        if self.moved == 0:
            possible_moves[1].append([self.position[0] + 2, self.position[1]])
            possible_moves[1].append([self.position[0] - 2, self.position[1]])
        return possible_moves
