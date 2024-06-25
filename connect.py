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


# Simple evaluation, whoever controls more square is better
# check nsew for pieces and sum their values, negates the values for yellow

YevenBonus = 4
YoddBonus = 2
RoddBonus = 5
RevenBonus = 0
RCenterBonus = 3
YCenterBonus = 3
RSideBonus = 2
YSideBonus = 2
RCornerBonus = -1
YCornerBonus = -1


def evalSquare(boardClass, row, col):
    board = boardClass.board
    score = 0

    ns = [0, 1, -1]
    ew = [0, 1, -1]

    for i in ns:
        for j in ew:
            if i == 0 and j == 0:
                continue

            newRow = row + i
            newCol = col + i

            if newRow < 0 or newRow > 5 or newCol < 0 or newCol > 6:
                continue
            targetSquare = board[newRow][newCol]
            if (targetSquare == red):
                score += 1

            elif (targetSquare == yellow):
                score -= 1

    if score > 0 and row % 3 == 0:
        # Red has more control
        # claims even
        if row % 2 == 0:
            score += RevenBonus
        else:
            # claims odd
            score += RoddBonus
    elif score < 0:
        # Yellow has more control
        # claims even
        if row % 2 == 0:
            score -= YevenBonus
        else:
            # claims odd
            score -= YoddBonus

    pce = board[row][col]
    if pce is not noPce:
        if col == 3:
            # Center column
            # Controlling the center is key in winning connect 4
            if pce == red:
                score += RCenterBonus
            else:
                score -= YCenterBonus
        if col == 2 or col == 4:
            # Columns beside the center
            # There are several tricks with occupying those, also important
            if pce == red:
                score += RSideBonus
            else:
                score -= YSideBonus
        if col == 0 or col == 6:
            # Columns at the corner
            # Usually very bad unless it creates a strong threat so we give it a penalty
            if pce == red:
                score += RCornerBonus
            else:
                score -= YCornerBonus

    return score


def evalBoard(boardClass):
    score = 0
    for row in range(6):
        for col in range(7):
            score += evalSquare(boardClass, row, col)
    return score


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


boardClass = stdBoard()
openings = []

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

def generate_openings_perfd(boardClass, depth):
    if depth == 0:
        return 1
    nodes = 0
    legals = moveGen(boardClass)
    for col in legals:
        boardClass = addPiece(boardClass, col)
        openings.append(chash(boardClass))
        nodes += generate_openings_perfd(boardClass, depth - 1)
        boardClass = undoMove(boardClass, col)
    return nodes


def generate_openings(boardClass, maxDepth):
    startTime = time.time()
    for depth in range(1, maxDepth + 1):
        nodes = generate_openings_perfd(boardClass, depth)
        elapsed = time.time() - startTime

generate_openings(boardClass, 6)

states = []
wdl = []
filtered_openings = list(set(openings))

print(len(filtered_openings))
'''
with open("openings_depth6_nostart.txt", "w") as f:
    for i in range(len(filtered_openings)):
        f.write(f"{filtered_openings[i]}\n")
'''

for i in range(len(filtered_openings)):
    print(f"Starting game {i+1}")
    moves = 0
    result = 0.0
    boardClass = stdBoard()
    boardClass = parse_board(boardClass, filtered_openings[i])
    while True:
        potentialWin = checkWin(boardClass)
        if (potentialWin is not noPce):
            result = 1.0 if potentialWin == red else 0.0
            break

        if len(moveGen(boardClass)) == 0:
            result = 0.5
            break

        moves += 1
        states.append(chash(boardClass))
        negamax(boardClass, 2, 0, -100000, 1000000)
        boardClass = addPiece(boardClass, bestMove)

    for _ in range(moves):
        wdl.append(result)

print(f"States Length: {len(states)}")
print(f"WDL Length: {len(wdl)}")

import csv

# Specify the file name
file_name = 'connect4_depth2_openingsd6nostart.csv'

# Combine lists into a list of tuples for easier CSV writing
data = list(zip(states, wdl))

# Write to CSV
with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write headers if needed
    writer.writerow(['states', 'wdl'])

    # Write data
    writer.writerows(data)

print(f'Data saved to {file_name}')
