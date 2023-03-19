import random
from abc import ABC, abstractmethod
import math
from anytree import Node

class Player(ABC) :
    def __init__(self,name) :
        self.name = name
        self.number = 0
    
    @abstractmethod
    def moveChoice(self,board,clickedColumn = None):
        pass
    

class RandomPlayer(Player) :
    def moveChoice(self,board) : 
        return random.randint(1,board.cols)


class ConsolePlayer(Player) :
    def moveChoice(self,board) : 
        while(True) :
            column = input("Play in which column ? : ").strip()
            if column.isdigit() :
                return int(column)
            else : 
                print("invalid entry")

class InterfacePlayer(Player) :
    def moveChoice(self,board,clickedColumn) : 
        return clickedColumn

class MinMaxPlayer(Player) :

    def __init__(self, name, depth = 7):
        super().__init__(name)
        self.depth = depth

    def moveChoice(self,board) :  
        if board.winNextMove() > 0 :
            return board.winNextMove()
        if board.turnplayed == 0 : return 4

        values = [-1000000] * board.cols

        for i in range(board.cols) :
            if board.firstfreerow[i] < board.rows :
                nb = board.clone()
                nb.play(i+1)
                values[i] = self.minmax(nb,self.depth-1,-100000,100000,False) 
        
        print(values)
        return values.index(max(values)) + 1
   
    def minmax(self,board, depth : int, alpha : int, beta : int, maximizing_player : bool) -> float :
         
         if board.checkWin() >= 0 : #winning board
             return 100000 if not maximizing_player else -100000
         elif board.turnplayed == board.draw : #draw
             return 0
         elif depth == 0 :
             return self.evaluate(board)
   
         if(maximizing_player) :
             value = - 100000
             for i in range(board.cols) :
                 if board.firstfreerow[i] < board.rows :
                     nb = board.clone()
                     nb.play(i+1)
                     minimax = self.minmax(depth=depth-1,alpha=alpha,beta=beta,board=nb,maximizing_player=False)
                     value = value if value > minimax else minimax
                     if value >= beta : return value
                     alpha = value if value > alpha else alpha
         else :
             value = 100000
             for i in range(board.cols) :
                 if board.firstfreerow[i] < board.rows :
                     nb = board.clone()
                     nb.play(i+1)
                     minimax = self.minmax(depth=depth-1,alpha=alpha,beta=beta,board=nb,maximizing_player=True)
                     value = value if value < minimax else minimax
                     if value <= alpha : return value
                     beta = value if value < beta else beta

         return value

        
    def evaluate(self,board) -> float :
        scoreboardplayer = 0
        scoreotherplayer = 0

        i,j = 0,0
        
        #score rows
        #if OOO : check if right or left is empty, OO : if OO-O or O-OO then 3, if --OO or OO-- then 2
        # 1 : if O--- or O--- then 1, if O--O or O-O- or -O-O then 2 
        while i < board.rows :
            while j < board.cols:
                symbol = board.grille[i][j]
                if symbol >= 0 :

                    othersymbol = 1 - symbol
                    originalj = j
                    winright,winleft = 0,0
                    
                    count = 1
                    j+=1
                    
                    while j < board.cols and board.grille[i][j] == symbol :
                        count *=10
                        j += 1

                    countright,countleft = count,count
                    aligned = j - originalj

                    if aligned == 3 : #3 in a row
                        if j < board.cols and board.grille[i][j] == -1 : winright = 1
                        if originalj > 0 and board.grille[i][originalj -1] == - 1 : winleft = 1
                    elif aligned == 2 :
                        if j < board.cols - 1 :
                            if board.grille[i][j] == -1 and board.grille[i][j + 1] != othersymbol :
                                winright = 1
                                if board.grille[i][j+1] == symbol : countright *= 10
                        if originalj > 1 : 
                            if board.grille[i][originalj - 1] == -1 and board.grille[i][originalj - 2] != othersymbol :
                                winleft = 1
                                if board.grille[i][originalj - 2] == symbol : countleft *= 10
                        if originalj > 0 and j < board.cols and winleft + winright == 0 :
                            if board.grille[i][originalj-1] == -1 and board.grille[i][j] == -1 :
                                winleft = 1
                    else :
                        if originalj > 2 :
                            if board.grille[i][originalj-2] != othersymbol and board.grille[i][originalj-1] == -1 and board.grille[i][originalj-3] == -1 :
                                winleft = 1
                                if board.grille[i][originalj-2] == symbol :
                                    countleft *= 10
                        if j < board.cols - 2 :
                            
                            if board.grille[i][j] == -1 and board.grille[i][j+1] != othersymbol and board.grille[i][j+2] != othersymbol :
                                winright = 1
                                if ((board.grille[i][j+1] == symbol) ^ (board.grille[i][j+2] == symbol)) :
                                    countright *= 10

                    if symbol == self.number :
                        scoreboardplayer += winleft * countleft + winright * countright
                    else :
                        scoreotherplayer += winleft * countleft + winright * countright
                else :
                    j += 1
            i += 1
            j = 0
        
        #score cols

        i,j = 0,0

        while i < board.cols :
            while j < board.rows - 3 :
                symbol = board.grille[j][i]
                othersymbol = 1 - symbol
                if symbol >= 0 and board.grille[j+1][i] != othersymbol and board.grille[j+2][i] != othersymbol  and board.grille[j+3][i] != othersymbol :
                    count = 1
                    j+=1
                    while j < board.rows and board.grille[j][i] == symbol :
                        j += 1
                        count *= 10

                    if symbol == self.number :
                        scoreboardplayer += count
                    else :
                        scoreotherplayer += count
                else :
                    j += 1
            i += 1
            j = 0

        #score diagonals

        #top left to bottom right, column

        i,j = 3,0
        counti = 3

        while i < board.rows :
            while i >= 0 :
                symbol = board.grille[i][j]
                originali = i
                originalj = j
                if symbol >= 0 :
                    count = 1
                    othersymbol = 1 - symbol
                    winleft,winright = 0,0
                    
                    
                    while i > 0 and board.grille[i-1][j+1] == symbol :
                        count *=10
                        j += 1
                        i -= 1

                    countright,countleft = count,count
                    aligned = originali - i + 1

                    if aligned == 3 :
                        if originalj > 0 :
                            if board.grille[originali + 1][originalj - 1] == -1 :
                                winleft = 1
                        if i > 0:
                            if board.grille[i - 1][j + 1] == -1 :
                                winright = 1
                    elif aligned == 2 :
                        if originalj > 1 :
                            if board.grille[originali + 1][originalj - 1] == -1 and board.grille[originali + 2][originalj - 2] != othersymbol :
                                winleft = 1
                                if board.grille[originali + 2][originalj - 2] == symbol : countleft *= 10
                        if i > 1 : 
                            if board.grille[i - 1][j + 1] == -1 and board.grille[i - 2][j + 2] != othersymbol :
                                winright = 1
                                if board.grille[i - 2][j + 2] == symbol : countright *= 10
                        if originalj > 0 and i > 0 and winleft + winright == 0 :
                            if board.grille[originali + 1][originalj - 1] == -1 and board.grille[i - 1][j + 1] == -1 :
                                winleft = 1
                    else :
                        if j > 2 :
                            if board.grille[i+2][j-2] != othersymbol and board.grille[i+3][j-3] == -1 and board.grille[i+1][j-1] == -1 :
                                winleft = 1
                                if board.grille[i+2][j-2] == symbol  :
                                    countleft *=10
                        if i > 2 :
                            if board.grille[i-1][j+1] == -1 and board.grille[i-2][j+2] != othersymbol and board.grille[i-3][j+3] != othersymbol:
                                winright = 1
                                if ((board.grille[i-2][j+2] == symbol) ^ (board.grille[i-3][j+3] == symbol)) :
                                    countright *= 10

                        
                    if symbol == self.number :
                        scoreboardplayer += countright * winright + countleft * winleft
                    else :
                        scoreotherplayer += countright * winright + countleft * winleft
               
                i -= 1
                j += 1
                                        
            i = counti + 1
            counti += 1
            j = 0
            
        #top left to bottom right, rows

        i,j = board.rows-1,1
        countj = 1

        while j < board.cols - 3 :
            while j < board.cols:
                symbol = board.grille[i][j]
                originali = i
                originalj = j  
                if symbol >= 0 :
                    count = 1
                    othersymbol = 1 - symbol
                    winleft,winright = 0,0
                    countright,countleft = count,count

                    while j < board.cols - 1 and board.grille[i-1][j+1] == symbol :
                        count *=10
                        j += 1
                        i -= 1

                    countright,countleft = count,count
                    aligned = originali - i + 1

                    if aligned == 3 :
                        if originali < board.rows - 1 :
                            if board.grille[originali + 1][originalj - 1] == -1 :
                                winleft = 1
                        if j < board.cols - 1:
                            if board.grille[i - 1][j + 1] == -1 :
                                winright = 1
                    elif aligned == 2 :
                        if originali < board.rows - 2 :
                            if board.grille[originali + 1][originalj - 1] == -1 and board.grille[originali + 2][originalj - 2] != othersymbol :
                                winleft = 1
                                if board.grille[originali + 2][originalj - 2] == symbol : countleft *= 10
                        if j < board.cols - 2 : 
                            if board.grille[i - 1][j + 1] == -1 and board.grille[i - 2][j + 2] != othersymbol :
                                winright = 1
                                if board.grille[i - 2][j + 2] == symbol : countright *= 10
                        if originali < board.rows - 1 and j < board.cols - 1 and winleft + winright == 0 :
                            if board.grille[originali + 1][originalj - 1] == -1 and board.grille[i - 1][j + 1] == -1 :
                                winleft = 1
                    else :
                        if i < board.rows - 3 :
                            if board.grille[i+2][j-2] != othersymbol and board.grille[i+1][j-1] == -1 and board.grille[i+3][j-3] == -1 :
                                winleft = 1
                                if board.grille[i+2][j-2] == symbol :
                                    countleft *= 10
                        if j < board.cols -  3:
                            if board.grille[i-1][j+1] == -1 and board.grille[i-2][j+2] != othersymbol and board.grille[i-3][j+3] != othersymbol:
                                winright = 1
                                if ((board.grille[i-2][j+2] == symbol) ^ (board.grille[i-3][j+3] == symbol)) :
                                    countright *= 10

                        
                    if symbol == self.number :
                        scoreboardplayer += countright * winright + countleft * winleft
                    else :
                        scoreotherplayer += countright * winright + countleft * winleft
                
                i -= 1
                j += 1
                                     
            i = board.rows - 1
            j = countj +  1
            countj += 1

        #bottom left to top right, column

        i,j = board.rows - 4,0
        counti = i

        while i >= 0 :
            while i < board.rows :
                symbol = board.grille[i][j]
                originali = i
                originalj = j
                if symbol >= 0 :
                    count = 1
                    othersymbol = 1 - symbol
                    winleft,winright = 0,0
                    
                    
                    while i < board.rows - 1 and board.grille[i+1][j+1] == symbol :
                        count *=10
                        j += 1
                        i += 1

                    countright,countleft = count,count
                    aligned = i - originali + 1

                    if aligned == 3 :
                        if originalj > 0 :
                            if board.grille[originali - 1][originalj - 1] == -1 :
                                winleft = 1
                        if i < board.rows - 1:
                            if board.grille[i + 1][j + 1] == -1 :
                                winright = 1
                    elif aligned == 2 :
                        if originalj > 1 :
                            if board.grille[originali - 1][originalj - 1] == -1 and board.grille[originali - 2][originalj - 2] != othersymbol :
                                winleft = 1
                                if board.grille[originali - 2][originalj - 2] == symbol : countleft *= 10
                        if i < board.rows -  2 : 
                            if board.grille[i + 1][j + 1] == -1 and board.grille[i + 2][j + 2] != othersymbol :
                                winright = 1
                                if board.grille[i + 2][j + 2] == symbol : countright *= 10
                        if originalj > 0 and i < board.rows - 1 and winleft + winright == 0 :
                            if board.grille[originali - 1][originalj - 1] == -1 and board.grille[i + 1][j + 1] == -1 :
                                winleft = 1
                        
                    else :
                        if j > 2 :
                            if board.grille[i-2][j-2] != othersymbol and board.grille[i-3][j-3] == -1 and board.grille[i-1][j-1] == -1 :
                                winleft = 1
                                if board.grille[i-2][j-2] == symbol  :
                                    countleft *=10
                        if i < board.rows -  3 :
                            if board.grille[i+1][j+1] == -1 and board.grille[i+2][j+2] != othersymbol and board.grille[i+3][j+3] != othersymbol:
                                winright = 1
                                if ((board.grille[i+2][j+2] == symbol) ^ (board.grille[i+3][j+3] == symbol)) :
                                    countright *= 10

                        
                    if symbol == self.number :
                        scoreboardplayer += countright * winright + countleft * winleft
                    else :
                        scoreotherplayer += countright * winright + countleft * winleft
               
                i += 1
                j += 1
                                        
            i = counti - 1
            counti -= 1
            j = 0
        
        #bottom left to top right, rows

        i,j = 0,1
        countj = 1

        while j < board.cols - 3 :
            while j < board.cols:
                symbol = board.grille[i][j]
                originali = i
                originalj = j  
                if symbol >= 0 :
                    count = 1
                    othersymbol = 1 - symbol
                    winleft,winright = 0,0
                    countright,countleft = count,count

                    while j < board.cols - 1 and board.grille[i+1][j+1] == symbol :
                        count *=10
                        j += 1
                        i += 1

                    countright,countleft = count,count
                    aligned = i - originali + 1

                    if aligned == 3 :
                        if originali > 0 :
                            if board.grille[originali - 1][originalj - 1] == -1 :
                                winleft = 1
                        if j < board.cols - 1:
                            if board.grille[i + 1][j + 1] == -1 :
                                winright = 1
                    elif aligned == 2 :
                        if originali > 1 :
                            if board.grille[originali - 1][originalj - 1] == -1 and board.grille[originali - 2][originalj - 2] != othersymbol :
                                winleft = 1
                                if board.grille[originali - 2][originalj - 2] == symbol : countleft *= 10
                        if j < board.cols - 2 : 
                            if board.grille[i + 1][j + 1] == -1 and board.grille[i + 2][j + 2] != othersymbol :
                                winright = 1
                                if board.grille[i + 2][j + 2] == symbol : countright *= 10
                        if originali > 0 and j < board.cols - 1 and winleft + winright == 0 :
                            if board.grille[originali - 1][originalj - 1] == -1 and board.grille[i + 1][j + 1] == -1 :
                                winleft = 1
                    else :
                        if i > 2 :
                            if board.grille[i-2][j-2] != othersymbol and board.grille[i-1][j-1] == -1 and board.grille[i-3][j-3] == -1 :
                                winleft = 1
                                if board.grille[i-2][j-2] == symbol :
                                    countleft *= 10
                        if j < board.cols -  3:
                            if board.grille[i+1][j+1] == -1 and board.grille[i+2][j+2] != othersymbol and board.grille[i+3][j+3] != othersymbol:
                                winright = 1
                                if ((board.grille[i+2][j+2] == symbol) ^ (board.grille[i+3][j+3] == symbol)) :
                                    countright *= 10

                        
                    if symbol == self.number :
                        scoreboardplayer += countright * winright + countleft * winleft
                    else :
                        scoreotherplayer += countright * winright + countleft * winleft
                
                i += 1
                j += 1
                                     
            i = 0
            j = countj +  1
            countj += 1

        return scoreboardplayer - scoreotherplayer

    
         
class MCSTPlayer(Player) :
    def __init__(self, name, iter = 1000,c = 1.414):
        super().__init__(name)
        self.iter = iter
        self.c = c

    def moveChoice(self,board) : 
        if board.winNextMove() >= 0 :
            return board.winNextMove()
        if board.turnplayed == 0 : return 4
        
        newboard = board.clone()
        values = self.MCST(newboard)
        return values.index(max(values)) + 1

    #calculate the upper confidence bound value of a node
    def UCB1(self,played : int, won : int,N : int) -> float :
        if played == 0 : return math.inf
        return won / played + self.c * math.sqrt(math.log(N)/played)
    
    def MCST(self,board) -> list[int] :
        root = Node("0",board=board,won=0,played=1)
        denom = [0] * board.cols

        #create children of root
        for i in range(board.cols) :
            if(board.firstfreerow[i] < board.rows) :
                nb = board.clone()
                nb.play(i+1)
                Node("0"+ str(i),board=nb,won=0,played=0,parent=root)
            else :
                denom[i] = -10000 #if the move is not possible

        iteration = self.iter

        while(iteration > 0) :

            currentNode : Node = root
            
            #finding a leaf node
            while (len(currentNode.children) > 0) :
                succUCB = []
                for succ in currentNode.children :
                    succUCB.append(self.UCB1(played=succ.played,won=succ.won,N=currentNode.played))
                
                currentNode = currentNode.children[succUCB.index(max(succUCB))] #choose the node with max UBC
            
            if currentNode.board.checkWin() < 0 and currentNode.board.turnplayed < board.draw: #if board is not a final board

                #creating children
                for i in range(board.cols) :
                    if(currentNode.board.firstfreerow[i] < board.rows) :
                        nb = currentNode.board.clone()
                        nb.play(i + 1)
                        Node(currentNode.name + str(i),board=nb,won=0,played=0,parent=currentNode)
                    
                #selecting a random son
                
                selectedson = currentNode.children[random.randint(0,len(currentNode.children) - 1)]

                #random playout
                start = selectedson.board.clone()
                while start.checkWin() < 0 and start.turnplayed < start.draw :
                    start.play(random.randint(1,start.cols))
            
                if start.turnplayed == start.draw : #if draw
                    won = 0
                else :
                    won = 1 if self.name != start.player.name else -1
            else :
                selectedson = currentNode
                if currentNode.board.turnplayed == board.draw :
                    won = 0
                else :
                    won = 1 if self.name != currentNode.board.player.name else -1

            #backpropagate
            #won = 1 if mcst won, -1 if lose, and 0 if draw (nothing is done in case of draw for won value)
            while selectedson != root :
                selectedson.played += 1
                if won == 1:
                    if selectedson.board.player.name != self.name : 
                        selectedson.won += 1
                    else : 
                        selectedson.won -= 3
                elif won == -1 :
                    if selectedson.board.player.name != self.name : 
                        selectedson.won -= 3
                    else : 
                        selectedson.won += 1

                selectedson = selectedson.parent
            
            root.played += 1

            iteration -= 1

        #prepare denom array
        count = 0

        for i in range(board.cols) :
            if denom[i] >= 0 : #if the move is possible
                denom[i] = root.children[count].played
                count += 1
                
        return denom


