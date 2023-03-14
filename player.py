import random
from abc import ABC, abstractmethod
import math
from anytree import Node,RenderTree

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
        if board.winNextMove() >= 0 :
            return board.winNextMove()
        
        values = [-1000] * board.cols

        for i in range(board.cols) :
            if board.firstfreerow[i] < board.rows :
                nb = board.clone()
                values[i] = self.minmax(nb.play(i),self.depth-1,-math.inf,math.inf,False) 
        
        return values.index(max(values)) + 1

    def evaluate(self,board) -> float :
        scoreboardplayer = 0
        playernumber = board.player.number
        scorepotherplayer = 0

        i,j = 0,0
        
        #score rows
        while i < board.rows :
            while j < board.cols :
                count = 0
                symbol = board.grille[i][j]
                freeleft = 1 if j > 0 and board.grille[i][j -1] == -1 else 0

                if symbol > 0 :
                    while board.grille[i][j] == symbol and j < board.cols :
                        j += 1
                        count +=1
                    
                    freeright = 1 if j < board.cols and board.grille[i][j] == -1 else 0

                    if symbol == board.player.number :
                        scoreboardplayer += (freeright+freeleft)*math.pow(10,count-1)
                    else :
                        scorepotherplayer += (freeright+freeleft)*math.pow(10,count-1)
                else :
                    j += 1
            i += 1


                


    
    def minmax(self,board, depth : int, alpha : int, beta : int, maximizing_player : bool) -> int :
         
         if board.checkWin () > 0 : #winning board
             return 1000 if not maximizing_player else -1000
         elif board.turnplayed == board.cols * board.rows : #draw
             return 0
         elif depth == 0 :
             return self.evaluate(board)
         
   
         if(maximizing_player) :
             value = - math.inf
             for i in range(board.cols) :
                 if board.firstfreerow[i] < board.cols :
                     nb = board.clone()
                     nb.play(i+1)
                     minimax = self.minmax(depth=depth-1,alpha=alpha,beta=beta,board=nb,maximizing_player=False)
                     value = value if value > minimax else minimax
                     if value >= beta : return value
                     alpha = value if value > alpha else alpha
         else :
             value = math.inf
             for i in range(board.cols) :
                 if board.firstfreerow[i] < board.cols :
                     nb = board.clone()
                     nb.play(i+1)
                     minimax = self.minmax(depth=depth-1,alpha=alpha,beta=beta,board=nb,maximizing_player=True)
                     value = value if value < minimax else minimax
                     if value <= alpha : return value
                     beta = value if value < beta else beta

         return value
             
    
         

class MCSTPlayer(Player) :
    def __init__(self, name, iter = 1000,c = 1.414):
        super().__init__(name)
        self.iter = iter
        self.c = c

    def moveChoice(self,board) : 
        if board.winNextMove() >= 0 :
            return board.winNextMove()
        
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
            
            if currentNode.board.checkWin() < 0 and currentNode.board.turnplayed < board.cols * board.rows: #if board is not a final board

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
                while start.checkWin() < 0 and start.turnplayed < start.rows * start.cols :
                    start.play(random.randint(1,start.cols))
            
                if start.turnplayed == start.rows * start.cols : #if draw
                    won = 0
                else :
                    won = 1 if self.name != start.player.name else -1
            else :
                selectedson = currentNode
                if currentNode.board.turnplayed == board.rows * board.cols :
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


