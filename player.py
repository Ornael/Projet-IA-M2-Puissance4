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
    
    def minmax(self,board, depth : int, alpha : int, beta : int, maximizing_player : bool) -> int :
         return random.randint(1,7)

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
        print(values)
        return values.index(max(values)) + 1

    def UCB1(self,played : int, won : int,N : int) -> float :
        if played == 0 : return math.inf
        return won / played + self.c * math.sqrt(math.log(N)/played)
    
    def MCST(self,board) -> list[int] :

        root = Node("0",board=board,won=0,played=1)
        denom = [0] * board.cols

        for i in range(board.cols) :
            if(board.firstfreerow[i] < board.rows) :
                nb = board.clone()
                nb.play(i+1)
                Node("0"+ str(i),board=nb,won=0,played=0,parent=root)
            else :
                denom[i] = -1


        iteration = self.iter

        while(iteration > 0) :

            currentNode : Node = root
            
            #finding a leaf node
            while (len(currentNode.children) > 0) :
                succUCB = []
                for succ in currentNode.children :
                    succUCB.append(self.UCB1(played=succ.played,won=succ.won,N=currentNode.played))
                
                currentNode = currentNode.children[succUCB.index(max(succUCB))]
            
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
            
            won = True if self.name != start.player.name else False

            #backpropagate
            while selectedson != root :
                selectedson.played += 1
                if won :
                    if selectedson.board.player.name != self.name : 
                        selectedson.won += 1
                    else : 
                        selectedson.won -= 10
                else :
                    if selectedson.board.player.name != self.name : 
                        selectedson.won -= 10
                    else : 
                        selectedson.won += 1

                selectedson = selectedson.parent
            
            root.played += 1

            iteration -= 1

        #print(RenderTree(root))
         
        for children in root.children :
            print(children) 
        #prepare denom array
        count = 0

        for i in range(board.cols) :
            if denom[i] >= 0 :
                denom[i] = root.children[count].played
                count += 1
                
        return denom

    

if __name__ == '__main__' :
    root = Node("A")

    # Create some child nodes and add them to the root node
    b_node = Node("B", parent=root)
    c_node = Node("C", parent=root)

    print(len(root.children))