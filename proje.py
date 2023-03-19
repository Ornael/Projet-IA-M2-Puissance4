import copy
from player import Player,MinMaxPlayer,MCSTPlayer,ConsolePlayer
import math

class Board :
    def __init__(self,player1 : Player,player2: Player,rows = 6,cols = 7):
        self.grille : list[int] = []
        self.rows : int = rows if rows > 3 else 4
        self.cols : int = cols if cols > 3 else 4
        self.draw : int  = self.rows * self.cols
        self.firstfreerow = [0] * self.cols
        for i in range(self.rows):
            self.grille.append([-1] * self.cols)
        self.lastplay = (0,0)
        self.turnplayed : int = 0
        player1.number : int = 0
        player2.number : int = 1
        self.player1 = player1
        self.player2 = player2
        self.player = player1
    
    def getOtherPlayerName(self) :
        return self.player1.name if self.player == self.player2 else self.player2.name

    #console print of board with chosen symbols 
    def print(self,p0symbol = "O",p1symbol = "X") :
        board = ""
        for i in range(self.rows - 1,-1,-1) :
            for j in range(self.cols) : 
                board += "|"
                if self.grille[i][j] == 0 :
                    board += p0symbol
                elif self.grille[i][j] == 1 :
                    board += p1symbol
                else : 
                    board += " "
            board += "|\n"
        print(board)
    
    #clone a board with deepcopy function
    def clone(self): 
        return copy.deepcopy(self)

    #play a move in current game board
    def play(self,column) -> bool : 
        truecol = column - 1
        if column > self.cols or self.firstfreerow[truecol] >= self.rows :
            return False
        else :
            self.grille[self.firstfreerow[truecol]][truecol] = self.player.number
            self.lastplay = (self.firstfreerow[truecol],truecol)
            self.firstfreerow[truecol] +=1 
            self.player = self.player1 if self.player.number == 1 else self.player2
            self.turnplayed += 1
            return True

    #if win, return player number else -1
    def checkWin(self) -> int : 

        if self.turnplayed < 7  : return -1
    
        row, col = self.lastplay
        symbol = self.grille[row][col]

        #check vertical
        if row >= 3 : 
            if self.grille[row-1][col] == symbol and self.grille[row-2][col] == symbol and self.grille[row-3][col] == symbol : return symbol

        #check right and left
        sameright,sameleft = True,True
        countaligned = 1
        positionright,positionleft= col,col

        while sameright or sameleft :
            if sameright and positionright + 1 < self.cols and self.grille[row][positionright + 1] == symbol :
                positionright += 1
                countaligned += 1
            else : 
                sameright = False
            
            if sameleft and positionleft - 1 >= 0 and self.grille[row][positionleft - 1] == symbol :
                positionleft -= 1
                countaligned += 1
            else : 
                sameleft = False
        
        if countaligned > 3 : return symbol

        #left-up to right-bottom diagonal
        sameright,sameleft = True,True
        countaligned = 1
        p1row,p1col= row,col
        p2row,p2col = row,col

        while sameright or sameleft :
            p1row -= 1
            p1col += 1
            if sameright and p1row >= 0 and p1col < self.cols and self.grille[p1row][p1col] == symbol :
                countaligned += 1
            else : 
                sameright = False

            p2row +=1
            p2col -= 1

            if sameleft and p2row < self.rows and p2col >= 0 and self.grille[p2row][p2col] == symbol :
                countaligned += 1
            else :
                sameleft = False

        if countaligned > 3 : return symbol

        #left-bottom to right up diagonal
        sameright,sameleft = True,True
        countaligned = 1
        p1row,p1col= row,col
        p2row,p2col = row,col

        while sameright or sameleft :
            p1row += 1
            p1col += 1
            if sameright and p1row < self.rows and p1col < self.cols and self.grille[p1row][p1col] == symbol :
                countaligned += 1
            else : 
                sameright = False

            p2row -=1
            p2col -= 1

            if sameleft and p2row >= 0 and p2col >= 0 and self.grille[p2row][p2col] == symbol :
                countaligned += 1
            else :
                sameleft = False

        if countaligned > 3 : return symbol
        return -1
    
    #check if immediate win is possible
    def winNextMove(self) :
        for i in range(self.cols) :
            nb = self.clone()
            nb.play(i+1)
            if nb.checkWin() >= 0:
                return i+1       
        return -1
    
if __name__ == '__main__':
     board = Board(MCSTPlayer("Axel",4000,2),MinMaxPlayer("Lexa",depth=6),6,7)

     while board.checkWin() < 0 and board.turnplayed < board.draw :

         if board.play(board.player.moveChoice(board))  : #try to play, print if move successful
             print(board.getOtherPlayerName())
             print("played : ")
             board.print()

     if board.checkWin() >= 0 :
        print("Win : " + board.getOtherPlayerName())
     else :
        print("Draw")  


""" board = Board(ConsolePlayer("Axel"),MinMaxPlayer("Lexa",depth=6),6,7)


board.play(4)
board.play(4)
board.play(7)
board.play(7)
board.play(5)
board.play(5)

board.print()


print(board.player2.evaluate(board))  """
