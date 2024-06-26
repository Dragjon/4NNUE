from connect import *

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

boardClass = stdBoard()
openings = []

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

with open("openings_depth6_nostart.txt", "w") as f:
    for i in range(len(filtered_openings)):
        f.write(f"{filtered_openings[i]}\n")

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
