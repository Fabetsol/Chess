import pyxel

SCREEN_SIDE_LENGHT = 16*8

class NotAColor(Exception):pass
class NotAPiece(Exception):pass

def is_on_board(position:tuple)->bool:
    y,x = position
    return (0<=y<=8 and 0<=x<=1)

class Piece:
    def __init__(self, name:str, y:int, x:int, color:bool, chessboard) -> None:
        self.name = name
        
        self.y = y
        self.x = x

        self.chessboard = chessboard

        if color in [-1, 1]:
            self.color = color
        else:
            raise NotAColor("Color must be equel to 1 or -1")
    
    def is_on_board(self, position:tuple)->bool:
        y,x = position
        return (0<=y<8 and 0<=x<8)
    
    def is_piece(self, position)->bool:
        y,x = position
        return type(self.chessboard.board[y][x]) != int
    
    def is_opposite_color(self, position:tuple)->bool:
        y,x = position
        if type(self.chessboard.board[y][x]) != int:
            return self.chessboard.board[y][x].color != self.color
        else:
            raise NotAPiece("There is no piece at that position")

class Pawn(Piece):
    def __init__(self, y:int, x:int, color:int, chessboard) -> None:
        super().__init__("pawn", y, x, color, chessboard)
    
    def available_moves(self)->list:

        infront = (self.y+self.color, self.x)
        if self.is_on_board(infront) and not self.is_piece(infront):
            yield infront
        
        front_side_1 = (self.y+self.color, self.x-1)
        if self.is_on_board(front_side_1) and self.is_piece(front_side_1) and self.is_opposite_color(front_side_1):
            yield front_side_1

        front_side_2 = (self.y+self.color, self.x+1)
        if self.is_on_board(front_side_2) and self.is_piece(front_side_2) and self.is_opposite_color(front_side_2):
            yield front_side_2

class Rook(Piece):
    def __init__(self, y:int, x:int, color:int, chessboard) -> None:
        super().__init__("rook", y, x, color, chessboard)
    
    def available_moves(self)->list:
        #up
        for y in range(1,8):
            move = (self.y+self.color*y, self.x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
        
        #down
        for y in range(1,8):
            move = (self.y-self.color*y, self.x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
        
        #right
        for x in range(1,8):
            move = (self.y, self.x+x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
        
        for x in range(1,8):
            move = (self.y, self.x-x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break

class Knight(Piece):
    def __init__(self, y:int, x:int, color:int, chessboard) -> None:
        super().__init__("knight", y, x, color, chessboard)
    
    def available_moves(self)->list:
        for y,x in zip([2,2,1,-1,-2,-2,-1,1],[-1,1,2,2,1,-1,-2,-2]):
            move = (self.y+y,self.x+x)
            if self.is_on_board(move) and (not self.is_piece(move) or self.is_opposite_color(move)):
                yield move

class Bishop(Piece):
    def __init__(self, y:int, x:int, color:int, chessboard) -> None:
        super().__init__("bishop", y, x, color, chessboard)
    
    def available_moves(self)->list:
        for y,x in zip([1,1,-1,-1],[1,-1,-1,1]):
            for i in range(1,8):
                move = (self.y+i*y, self.x+i*x)
                if self.is_on_board(move):
                    if not self.is_piece(move):
                        yield move
                    elif self.is_opposite_color(move):
                        yield move
                        break
                    else:
                        break
                else:
                    break
                
class King(Piece):
    def __init__(self, y:int, x:int, color:int, chessboard) -> None:
        super().__init__("king", y, x, color, chessboard)
    
    def available_moves(self)->list:
        for y,x in zip([1,1,1,0,-1,-1,-1,0],[-1,0,1,1,1,0,-1,-1]):
            move = (self.y+y,self.x+x)
            if self.is_on_board(move) and (not self.is_piece(move) or self.is_opposite_color(move)):
                yield move

class Queen(Piece):
    def __init__(self, y:int, x:int, color:int, chessboard) -> None:
        super().__init__("queen", y, x, color, chessboard)
    
    def available_moves(self)->list:
        #up
        for y in range(1,8):
            move = (self.y+self.color*y, self.x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
        
        #down
        for y in range(1,8):
            move = (self.y-self.color*y, self.x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
        
        #right
        for x in range(1,8):
            move = (self.y, self.x+x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
        
        for x in range(1,8):
            move = (self.y, self.x-x)
            if self.is_on_board(move):
                if not self.is_piece(move):
                    yield move
                elif self.is_opposite_color(move):
                    yield move
                    break
                else:
                    break
            else:
                break
    
        for y,x in zip([1,1,-1,-1],[1,-1,-1,1]):
                for i in range(1,8):
                    move = (self.y+i*y, self.x+i*x)
                    if self.is_on_board(move):
                        if not self.is_piece(move):
                            yield move
                        elif self.is_opposite_color(move):
                            yield move
                            break
                        else:
                            break
                    else:
                        break

class Chessboard:
    def __init__(self, screen_lenght) -> None:
        self.set_board()
        self.playable = [[0 for i in range(8)] for j in range(8)]

        self.white_turn = True

        pyxel.init(screen_lenght, screen_lenght, "Chess")
        pyxel.load("ressources.pyxres")
        pyxel.mouse(True)

        pyxel.run(self.draw, self.update)
    
    def set_board(self)->None:
        self.board = []

        self.board.append([Rook(0,0,1,self),Knight(0,1,1,self),Bishop(0,2,1,self),King(0,3,1,self),Queen(0,4,1,self),Bishop(0,5,1,self),Knight(0,6,1,self),Rook(0,7,1,self)]) #black big pieces
        self.board.append([Pawn(1,i,1,self) for i in range(8)]) #black pawns

        for i in range(4): self.board.append([0]*8) #four empty rows

        self.board.append([Pawn(6,i,-1,self) for i in range(8)]) #white pawns
        self.board.append([Rook(7,0,-1,self),Knight(7,1,-1,self),Bishop(7,2,-1,self),King(7,3,-1,self),Queen(7,4,-1,self),Bishop(7,5,-1,self),Knight(7,6,-1,self),Rook(7,7,-1,self)]) #white big pieces
    
    def remove_all_1(self)->None:
        for y in range(len(self.playable)):
            for x in range(len(self.playable[y])):
                self.playable[y][x] = 0 if self.playable[y][x]==1 else self.playable[y][x]

    def get_mouse_position(self)->tuple:
        y = pyxel.mouse_y//16
        x = pyxel.mouse_x//16
        return (y,x)

    def update(self)->None:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            y,x = self.get_mouse_position()
            if self.playable[y][x] == 1:
                self.board[y][x] = type(self.selected_piece)(y,x, self.selected_piece.color, self)
                self.board[self.selected_piece.y][self.selected_piece.x] = 0
                self.remove_all_1()

                self.white_turn = not self.white_turn

            if type(self.board[y][x]) != int:
                if (self.board[y][x].color<0)==self.white_turn:
                    self.remove_all_1()
                    self.selected_piece = self.board[y][x]
                    for move in list(self.selected_piece.available_moves()):
                        move_y,move_x = move
                        self.playable[move_y][move_x] = 1
        
    def draw(self)->None:
        pyxel.cls(0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if (x+y)%2 == 0:
                    pyxel.blt(x*16,y*16,0, 0,0,16,16)
                else:
                    pyxel.blt(x*16,y*16,0, 16,0,16,16)
                
                if self.playable[y][x] == 1:
                    pyxel.blt(x*16,y*16,0, 32,0,16,16, 10)

                if type(self.board[y][x]) != int:
                    color = 16 if self.board[y][x].color>0 else 0
                    if type(self.board[y][x]) == Pawn:
                        pyxel.blt(x*16,y*16,0, 0+color,16,16,16, 10)
                    elif type(self.board[y][x]) == Rook:
                        pyxel.blt(x*16,y*16,0, 32+color,16,16,16, 10)
                    elif type(self.board[y][x]) == Knight:
                        pyxel.blt(x*16,y*16,0, 0+color,32,16,16, 10)
                    elif type(self.board[y][x]) == Bishop:
                        pyxel.blt(x*16,y*16,0, 32+color,32,16,16, 10)
                    elif type(self.board[y][x]) == King:
                        pyxel.blt(x*16,y*16,0, 0+color,48,16,16, 10)
                    elif type(self.board[y][x]) == Queen:
                        pyxel.blt(x*16,y*16,0, 32+color,48,16,16, 10)

chessboard = Chessboard(SCREEN_SIDE_LENGHT)