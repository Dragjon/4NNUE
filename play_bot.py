##################################
# Connect 4 Game with a simple negamax ai
# Programmed in python by Dragjon
# Programmed in an airplane using a mobile phone
##################################
# Licence : MIT Licence
##################################

import time
import numpy as np
from tensorflow.keras.models import load_model

def flatten(boardClass):
    fen = []
    for i in range(len(boardClass.board)):
        for j in range(len(boardClass.board[0])):
            fen.append(boardClass.board[i][j])
    return fen

# Load the saved model
model = load_model('connect4_256x1_model.h5')

noPce = 0
red = 1
yellow = 2

class stdBoard():
    def __init__(self):
        self.board = [[noPce for _ in range(7)] for _ in range(6)]
        self.turn = red

def addPiece(boardClass, col):
    pce = boardClass.turn
    for row in range(6):
        if boardClass.board[row][col] != noPce:
            boardClass.board[row - 1][col] = pce
            break
        if row == 5 and boardClass.board[row][col] == noPce:
            boardClass.board[row][col] = pce
            break
    boardClass.turn = 3 - pce
    return boardClass

def undoMove(boardClass, col):
    for row in range(6):
        if boardClass.board[row][col] != noPce:
            boardClass.board[row][col] = noPce
            boardClass.turn = 3 - boardClass.turn
            return boardClass


def printBoard(boardClass):
    board = boardClass.board
    for i in range(6):
        for j in range(7):
            pce = board[i][j]
            pceChar = "- " if pce == noPce else "🔴" if pce == red  else "🟡"
            print(pceChar, end = " ")
        print()
        if i != 5:
            print()
    print("-------------------")
    print("1| 2| 3| 4| 5| 6| 7 ")
    print()

##########
#         N        #
#    W  o  E    #
#         S         #
##########
# N - [row - 1][col]
# S - [row + 1][col]
# E - [row][col+1]
# W - [row][col - 1]
# NE - [row - 1][col + 1]
# SE - [row + 1][col + 1]
# NW - [row - 1][col - 1]
# SW - [row + 1][col - 1]

# Idea:
# loop through all the pieces starting from [0, 0] then [0, 1] etc
# for each piece, check the following
#        - connect 4 in N, S, E or W
# after checking, if found, return a winner else noPce

def isConnect4(boardClass, row, col):
    board = boardClass.board
    pce = board[row][col] if board[row][col] is not noPce else None

    # Check North
    if row >= 3 and board[row - 1][col] == pce and board[row - 2][col] == pce and board[row - 3][col] == pce:
        return True

    # Check South
    if row <= 2 and board[row + 1][col] == pce and board[row + 2][col] == pce and board[row + 3][col] == pce:
        return True

    # Check East
    if col <= 3 and board[row][col + 1] == pce and board[row][col + 2] == pce and board[row][col + 3] == pce:
        return True

    # Check West
    if col >= 3 and board[row][col - 1] == pce and board[row][col - 2] == pce and board[row][col - 3] == pce:
        return True

    # Check Northeast
    if row >= 3 and col <= 3 and board[row - 1][col + 1] == pce and board[row - 2][col + 2] == pce and board[row - 3][col + 3] == pce:
        return True

    # Check Southeast
    if row <= 2 and col <= 3 and board[row + 1][col + 1] == pce and board[row + 2][col + 2] == pce and board[row + 3][col + 3] == pce:
        return True

    # Check Northwest
    if row >= 3 and col >= 3 and board[row - 1][col - 1] == pce and board[row - 2][col - 2] == pce and board[row - 3][col - 3] == pce:
        return True

    # Check Southwest
    if row <= 2 and col >= 3 and board[row + 1][col - 1] == pce and board[row + 2][col - 2] == pce and board[row + 3][col - 3] == pce:
        return True

    return False


def checkWin(boardClass):
    board = boardClass.board
    for row in range(6):
        for col in range(7):
            if(isConnect4(boardClass, row, col)):
                return board[row][col]

    return noPce

def moveGen(boardClass):
    moves = []
    board = boardClass.board
    for col in range(7):
        if board[0][col] == noPce:
            moves.append(col)
    return moves

def perfd(boardClass, depth):
    if depth == 0:
        return 1
    nodes = 0
    legals = moveGen(boardClass)
    for col in legals:
        boardClass = addPiece(boardClass, col)
        nodes += perfd(boardClass, depth - 1)
        boardClass = undoMove(boardClass, col)
    return nodes

def perft(boardClass, maxDepth):
    startTime = time.time()
    for depth in range(1, maxDepth + 1):
        nodes = perfd(boardClass, depth)
        elapsed = time.time() - startTime
        print(f"info string perft depth {depth} time {int(elapsed*1000)} nodes {nodes} nps {int(nodes / elapsed + 0.000000001)}")

import math
def sigmoid(x):
   return 1 / (1 + math.pow(math.e, -x)) 

# NNUE Evaluation
def evalBoard(boardClass, wdl = False):
    pos = np.array([flatten(boardClass)])
    predictions = model.predict(pos)
    if not wdl:
        return 100 * predictions[0, 0]
    else:
        return sigmoid(predictions[0, 0])

bestMove = None

def negamax(boardClass, depth, ply, alpha, beta):
    global bestMove
    if checkWin(boardClass) is not noPce:
        return -30000 + ply
    legals = moveGen(boardClass)
    if len(legals) == 0:
        return 0
    color = 1 if boardClass.turn == red else -1
    if depth == 0:
        return evalBoard(boardClass) * color
    max = -100000
    for col in legals:
        boardClass = addPiece(boardClass, col)
        score = -negamax(boardClass, depth - 1, ply + 1, -beta, -alpha)
        boardClass = undoMove(boardClass, col)

        if score > alpha:
            alpha = score

        if score > max:
            if ply == 0:
                bestMove = col
            max = score

        if score >= beta:
            break

    return max

boardClass = stdBoard()
print('''
   ______                            __        __ __
  / ____/___  ____  ____  ___  _____/ /_      / // /
 / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/_____/ // /_
/ /___/ /_/ / / / / / / /  __/ /__/ /_/_____/__  __/
\____/\____/_/ /_/_/ /_/\___/\___/\__/        /_/   

''')
turn = red if input("Start as 1st player (red 🔴) or 2nd player(yellow 🟡) [r/y]: ") == "r" else yellow
while True:
    printBoard(boardClass)
    potentialWin = checkWin(boardClass)
    if (potentialWin is not noPce):
        winnerChar = "Red" if potentialWin == red else "Yellow"
        print(f"{winnerChar} won by connecting 4!")
        break

    if len(moveGen(boardClass)) == 0:
        print("The game is drawn")

    if boardClass.turn == turn:
        col = int(input("Pick a column (1-7): "))
        boardClass = addPiece(boardClass, col - 1)
    else:
        eval = negamax(boardClass, 3, 0, -100000, 1000000)
        print(f"🤖 Computer evaluation: {eval}")
        print(f"WDL: {sigmoid(eval / 100)}")
        boardClass = addPiece(boardClass, bestMove)
