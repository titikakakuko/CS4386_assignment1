###############################
# CS4386 Semester B, 2021-2022
# Assignment 1
# Name: WANG Yinuo
# Student ID: 55670000
###############################
import copy 
from math import inf as INFINITY
from operator import ne
import random
import numpy as np
import time
# from game import alignement

def gridFull(grid):
    for rows in grid:
        for cell in rows:
            if cell is None:
                return False
    return True

def gridEmpty(grid):
    for rows in grid:
        for cell in rows:
            if cell is not None:
                return False
    return True

def alignement(grid,x,y):
    #print("xy:",x,y)
    score=0

    #1.check horizontal
    if((grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5]  != None)):  
        score+=6
        #print("horizontal 6")
    else:
        if (grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] == None):
            if y==0 or y==1 or y==2:
                score+=3
                #print("1horizontal 3")
        elif (grid[x][0] == None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] == None):
            if y==1 or y==2 or y==3:
                score+=3
                #print("2horizontal 3")
        elif  (grid[x][1] == None) and (grid[x][2] != None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] == None):
            if y==2 or y==3 or y==4:
                score+=3
                #print("3horizontal 3")
        elif  (grid[x][2] == None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] != None):
            if y==3 or y==4 or y==5:
                score+=3
                #print("4horizontal 3")
            
    #2.check vertical
    if((grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y]!= None) and (grid[5][y]!= None)):
        score+=6
        #print("vertical 6")
    else:
        if (grid[0][y] != None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] == None):
            if x==0 or x==1 or x==2:
                score+=3
                #print("1vertical 3")
        elif (grid[0][y] == None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] != None) and (grid[4][y] == None):
            if x==1 or x==2 or x==3:
                score+=3
                #print("2vertical 3")
        elif (grid[1][y] == None) and (grid[2][y] != None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] == None):
            if x==2 or x==3 or x==4:
                score+=3
                #print("3vertical 3")
        elif  (grid[2][y] == None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] != None):
            if x==3 or x==4 or x==5:
                score+=3
                #print("4vertical 3")


    return score


class Grid():
    def __init__(self, grid):
        # self.grid = np.full((6,6), None)
        self.grid = grid.copy()

    def update(self, x, y, symbol):
        if(self.grid[x][y] is None):
            self.grid[x][y] = symbol
            return True
        print("Cell already used!")
        return False

    def isMoveAllowed(self, x, y):
        return self.grid[x][y] is None

    def __str__(self):
        grid = ""
        for i, row in enumerate(self.grid):
            grid += "|"
            for j, cell in enumerate(row):
                if(cell is None):
                    grid += " -"
                else:
                    grid += " " + self.grid[i][j]
            grid += " |\n"
        return grid

class Board:
    def __init__(self, state, p1,p2,is_myturn):
        # state is the grid
        self.state = state
        self.p1=p1
        self.p2=p2
        # isMyturn indicates whether it is the p1's turn
        self.is_myturn = is_myturn
        self.res_ddl = 7
    
    def my_score(self):
        return self.p1.get_score()
    def opp_score(self):
        return self.p2.get_score()
    
    def evaluate(self):
        score = self.my_score() - self.opp_score()
        return (score if self.is_myturn else -score)

    def finished(self):
        return gridFull(self.state.grid)

    def showB(self):
        print(self.state.grid)

    def take_move(self, move):
        # take move according to the current game state
        playerTurn = self.p1.get_copy() if self.is_myturn else self.p2.get_copy()
        grid=Grid(self.state.grid)
        
        # update grid
        x, y = move[0], move[1]
        grid.update(x, y, playerTurn.get_symbole())

        # update score
        # (x, y) = move
        score = alignement(grid.grid,x,y)
        playerTurn.add_score(score)
        # if score>0:
        #     print(grid.grid)
        #     print(playerTurn.get_symbole(), ", move is:",x,y, ", score is:",score, " and ", playerTurn.get_score())
    
        # update isMyturn, return a new board
        if self.is_myturn:
            return Board(grid,playerTurn,self.p2.get_copy(),False)
        else:
            return Board(grid,self.p1.get_copy(),playerTurn,True)

    
    def get_legal_moves(self):
        # return a list of legal moves
        cells = []

        for x, row in enumerate(self.state.grid):
            for y, cell in enumerate(row):
                if cell is None:
                    cells.append([x, y])

        return cells

    def get_near_moves(self):
        # return a list of near moves(near the non-empty cells)
        cells = []
        pad_grid=np.pad(self.state.grid.copy(), ((2,2),(2,2)),'constant',constant_values = (None,None))
        is_First=True
        for x, row in enumerate(self.state.grid):
            for y, cell in enumerate(row):
                if cell is None:
                    is_empty=True
                    for i in range(-2,3):
                        for j in range(-2,3):
                            if pad_grid[x+2+i][y+2+j] is not None:
                                is_empty=False
                    if  not is_empty or is_First:
                        cells.append([x, y])
                        is_First = False

        return cells


def abnegamax(board, maxDepth, currentDepth, alpha, beta):
    if board.finished() or (maxDepth == currentDepth) :
        score = board.evaluate()
        return score, None
    
    bestMove = []
    bestScore = -INFINITY
    legal_moves = board.get_legal_moves()
    for move in legal_moves:
        newBoard = board.take_move(move)
        recursedScore = 0 
        currentScore = 0
        currentMove = None

        # recurse abnegamax, calculate the bestscore 
        (recursedScore, currentMove) = abnegamax(newBoard, maxDepth, currentDepth+1, -beta, -max(alpha, bestScore))
        currentScore = -recursedScore
        
        # Update the best score
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = [move]
                
        # If the branch outside the bounds, then prune
        if bestScore >= beta:
            return bestScore, bestMove
            
        # If there're same scores, store all the moves for randomizing
        if currentScore == bestScore:
            bestMove.append(move)
              
    return bestScore, bestMove

class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name
    def get_isAI(self):
        return self.isAI
    def get_symbole(self):
        return self.symbole
    def get_score(self):
        return self.score
    def add_score(self,score):
    	self.score+=score
    def get_copy(self):
        # copy = AIPlayer(self.name, self.symbole, self.isAI)
        # copy.add_score(self.score)
        # x = copy.copy(y) # make a shallow copy of y x = copy.deepcopy(y) # make a deep copy of y
        return copy.deepcopy(self)
    
    def empty_cells(self,state):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell is None:
                    cells.append([x, y])

        return cells

    def get_move(self,grid, player):
        # if myAI is the first player, then return a random step
        if gridEmpty(grid):
            return (random.randint(0, 5), random.randint(0, 5))
        
        # create two players and a grid for the board
        my_player = AIPlayer("myAI", player, isAI=False)
        opp_player = AIPlayer("opp", "X", isAI=False) 
        state=Grid(grid)
        board = Board(state, my_player, opp_player, True)

        # return good moves
        (bestScore, bestMoves) = abnegamax(board, 4, 0, -INFINITY, INFINITY)

        # try different best moves
        # idx = random.randint(0, len(bestMoves) - 1)
        # idx = len(bestMoves) - 1
        idx = 0
        return bestMoves[idx]


    