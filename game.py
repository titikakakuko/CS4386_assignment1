import numpy as np
import random
import ctypes, platform, time
from ctypes import *
import gui
import os,jpype
from jpype import *
import ctypes as ct
import sys
class Grid():
    def __init__(self):
        self.grid = np.full((6,6), None)

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

class Player():
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.won_games = 0
        self.draw_games = 0
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

def alignement(grid,x,y):
    #print("xy:",x,y)
    score=0

    #1.check horizontal
    if((grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5]  != None)):  
        score+=6
    else:
        if (grid[x][0] != None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] == None) :
            score+=3
        elif (grid[x][0] == None) and (grid[x][1] != None) and  (grid[x][2]!= None) and (grid[x][3] != None) and (grid[x][4] == None) :
            score+=3
        elif (grid[x][1] == None) and (grid[x][2] != None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] == None):
            score+=3
        elif (grid[x][2] == None) and  (grid[x][3]!= None) and (grid[x][4] != None) and (grid[x][5] != None):
            score+=3
            
    #2.check vertical
    if((grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y]!= None) and (grid[5][y]!= None)):
        score+=6
    else:
        if (grid[0][y] != None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] == None) :
            score+=3
        elif (grid[0][y] == None) and (grid[1][y] != None) and  (grid[2][y]!= None) and (grid[3][y] != None) and (grid[4][y] == None) :
            score+=3
        elif (grid[1][y] == None) and (grid[2][y] != None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] == None):
            score+=3
        elif (grid[2][y] == None) and  (grid[3][y]!= None) and (grid[4][y] != None) and (grid[5][y] != None):
            score+=3


    return score

def gridFull(grid):
    for rows in grid:
        for cell in rows:
            if cell is None:
                return False
    return True


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell is None:
                cells.append([x, y])
    #print(cells)
    return cells

def gameLoop(screen, p1, p2):

    def switchPlayer(turn):
        if(turn == p1):
            return p2
        return p1

    # Initiliaze the Grid
    grid = Grid()

    # Choose randomly a player
    if(random.randint(1, 2) ==1):
        playerTurn = p1
    else:
        playerTurn = p2

    # Check if player is AI
    if(playerTurn.get_isAI()):
        #1.if AI written in C++
        if language =="CPP":
            python_board=grid.grid
            char_arr2 = ctypes.c_char*6
            char_arr22 = char_arr2*6
            cpp_board = char_arr22()
            for row in range(6):
                for column in range(6):
                    if python_board[row][column]=="X":
                        cpp_board[row][column]=c_char(b"X")
                    elif python_board[row][column]=="O":
                        cpp_board[row][column]=c_char(b"O")	

            cpp_symbole= playerTurn.get_symbole()
            move = playerTurn.get_move(cpp_board, cpp_symbole)
            x, y = move.contents[0],move.contents[1]
            grid.update(x, y, chr(playerTurn.get_symbole()))
            gui.drawSymbole(screen, (x, y), chr(playerTurn.get_symbole()))
        #2.if AI written in JAVA
        elif language=="JAVA":
            python_board=grid.grid
            java_board = java.util.ArrayList()
            for row in range(6):
                row_board= java.util.ArrayList()
                for column in range(6):
                    row_board.add(python_board[row][column])
                java_board.add(row_board)
            move = playerTurn.get_move(java_board, playerTurn.get_symbole())
            x, y = move[0], move[1]
            grid.update(x, y, playerTurn.get_symbole())
            gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
        #3.if AI written in Python
        else:
            move = playerTurn.get_move(grid.grid, playerTurn.get_symbole())
            x, y = move[0], move[1]
            grid.update(x, y, playerTurn.get_symbole())
            gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            


    else:
        # Get player input
        x, y = gui.playerInput(screen)
        # Check if the cell is not already used
        while not grid.isMoveAllowed(x, y):
            x, y = gui.playerInput(screen)
        grid.update(x, y, playerTurn.symbole)
        gui.drawSymbole(screen, (x, y), playerTurn.symbole)

##    aligned, _ = alignement(grid.grid)
    while(not gridFull(grid.grid)):
        # Switch player
        playerTurn = switchPlayer(playerTurn)

        # Check if player is AI
        if(playerTurn.get_isAI()):
            #if written in c++
            if language =="CPP":
                python_board=grid.grid
                char_arr2 = ctypes.c_char*6
                char_arr22 = char_arr2*6
                cpp_board = char_arr22()
                for row in range(6):
                    for column in range(6):
                        if python_board[row][column]=="X":
                            cpp_board[row][column]=c_char(b"X")
                        elif python_board[row][column]=="O":
                            cpp_board[row][column]=c_char(b"O")
                cpp_symbole= playerTurn.get_symbole()
                move = playerTurn.get_move(cpp_board, cpp_symbole)
                x, y = move.contents[0],move.contents[1]
                grid.update(x, y, chr(playerTurn.get_symbole()))
                gui.drawSymbole(screen, (x,y), chr(playerTurn.get_symbole()))
            #if AI written in JAVA
            elif language=="JAVA":
                python_board=grid.grid
                java_board = java.util.ArrayList()
                for row in range(6):
                    row_board= java.util.ArrayList()
                    for column in range(6):
                        row_board.add(python_board[row][column])
                    java_board.add(row_board)
                move = playerTurn.get_move(java_board, playerTurn.get_symbole())
                x, y = move[0], move[1]
                grid.update(x, y, playerTurn.get_symbole())
                gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            else:
                move = playerTurn.get_move(grid.grid, playerTurn.get_symbole())
                x, y = move[0], move[1]
                grid.update(x, y, playerTurn.get_symbole())
                gui.drawSymbole(screen, (x,y), playerTurn.get_symbole())
            

            #check the score
            p_score = alignement(grid.grid,x,y)
            playerTurn.add_score(p_score)
            print("current score:",p1.get_score(),p2.get_score())
        else:
            # Get player input
            x, y = gui.playerInput(screen)
            # Check if the cell is not already used
            while not grid.isMoveAllowed(x, y):
                x, y = gui.playerInput(screen)
            grid.update(x, y, playerTurn.symbole)
            gui.drawSymbole(screen, (x, y), playerTurn.symbole)
            #check the score
            p_score = alignement(grid.grid,x,y)
            playerTurn.score+=p_score
            print("current score:",p1.get_score(),p2.get_score())

    
    if(p1.get_score()>p2.get_score()):
        return "Black"

    elif(p1.get_score()<p2.get_score()):
        return "Red"
    else:
        return "0"

if __name__ == "__main__":
    inpt = "y"
    # language= {CPP, JAVA,PYTHON}
    language=sys.argv[1]
    
    p1 = Player("vic", "X")
    #p1 = Player("AI1", "X", isAI=True)

    if language =="CPP":
        print("you are using C++")
        p2 = CDLL('./cpp/aiplayer.so')
        p2.add_symbole(c_char(b"O"))
        p2.get_move.restype = ctypes.POINTER(ctypes.c_int*2)
    elif language=="JAVA":
        print("you are using JAVA")
        jarpath = os.path.join(os.path.abspath('.'), 'java/AIPlayer.jar')
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)
        AIPlayer = jpype.JClass('com.AIPlayer')
        p2 = AIPlayer()
        p2.add_symbole("O")
    else:
        print("you are using Python")
        from python.studentid import AIPlayer
        p2 = AIPlayer("AI2", "O", isAI=True)
        

    
        
    
    screen = gui.init()

    while(inpt != "n"):

        # Start the game loop
        winner = gameLoop(screen, p1, p2)

        if(winner != "0"):
            gui.writeScreen(screen, winner+" Won", line=1)
 
        else:
            gui.writeScreen(screen, "Draw!", line=1)

        gui.writeScreen(screen, "Click to", line=2)
        gui.ask(screen, " play again!", line=3)
        gui.clearScreen(screen)

    jpype.shutdownJVM()
