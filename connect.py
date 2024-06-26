##################################
# Connect 4 Game with a simple negamax ai
# Programmed in python by Dragjon
# Programmed in an airplane using a mobile phone
##################################
# Licence : MIT Licence
##################################

import time

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
            pceChar = "- " if pce == noPce else "🔴" if pce == red else "🟡"
            print(pceChar, end=" ")
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
    if row >= 3 and board[row - 1][col] == pce and board[
            row - 2][col] == pce and board[row - 3][col] == pce:
        return True

    # Check South
    if row <= 2 and board[row + 1][col] == pce and board[
            row + 2][col] == pce and board[row + 3][col] == pce:
        return True

    # Check East
    if col <= 3 and board[row][col + 1] == pce and board[row][
            col + 2] == pce and board[row][col + 3] == pce:
        return True

    # Check West
    if col >= 3 and board[row][col - 1] == pce and board[row][
            col - 2] == pce and board[row][col - 3] == pce:
        return True

    # Check Northeast
    if row >= 3 and col <= 3 and board[row - 1][col + 1] == pce and board[
            row - 2][col + 2] == pce and board[row - 3][col + 3] == pce:
        return True

    # Check Southeast
    if row <= 2 and col <= 3 and board[row + 1][col + 1] == pce and board[
            row + 2][col + 2] == pce and board[row + 3][col + 3] == pce:
        return True

    # Check Northwest
    if row >= 3 and col >= 3 and board[row - 1][col - 1] == pce and board[
            row - 2][col - 2] == pce and board[row - 3][col - 3] == pce:
        return True

    # Check Southwest
    if row <= 2 and col >= 3 and board[row + 1][col - 1] == pce and board[
            row + 2][col - 2] == pce and board[row + 3][col - 3] == pce:
        return True

    return False


def checkWin(boardClass):
    board = boardClass.board
    for row in range(6):
        for col in range(7):
            if (isConnect4(boardClass, row, col)):
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
        print(
            f"info string perft depth {depth} time {int(elapsed*1000)} nodes {nodes} nps {int(nodes / elapsed + 0.000000001)}"
        )

def chash(boardClass):
    fen = ""
    for i in range(len(boardClass.board)):
        for j in range(len(boardClass.board[0])):
            fen += str(boardClass.board[i][j])
    return fen

def flatten(boardClass):
    fen = []
    for i in range(len(boardClass.board)):
        for j in range(len(boardClass.board[0])):
            fen.append(boardClass.board[i][j])
    return fen

def parse_board(boardClass, fen):
    i = 0
    j = 0
    
    for char in fen:
        if i == 7:
            i = 0
            j += 1

        boardClass.board[j][i] = int(char)
        i += 1

    return boardClass
