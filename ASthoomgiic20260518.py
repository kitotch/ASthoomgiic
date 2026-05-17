import copy

#先手: 1
#後手: 0

piecesMove = {
    "_p": [(0, -1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "_l": [(0, -1, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "_n": [(1, -2, 0), (-1, -2, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "_s": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "_g": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0)],
    "_b": [(-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "_r": [(0, -1, 1), (-1, 0, 1), (1, 0, 1), (0, 1, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "_k": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (-1, 1, 0), (0, 1, 0), (1, 1, 0)],
    "+p": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0)],
    "+l": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0)],
    "+n": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0)],
    "+s": [(-1, -1, 0), (0, -1, 0), (1, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0)],
    "+g": [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    "+b": [(-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0)],
    "+r": [(0, -1, 1), (-1, 0, 1), (1, 0, 1), (0, 1, 1), (-1, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 1, 0)],
    "+k": [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
}

startpos = "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1"

def decodeSFEN(sfen):
    board = [[]]
    hand = [[0] * 7 for i in range(2)]
    now = 0
    emptyCount = 0
    handCount = 0
    promoteFlag = False
    turn = None
    moves = 0
    for s in sfen:
        if now == 0:
            if s == " ":
                now += 1
            elif s == "/":
                board[-1].extend(["___"] * emptyCount)
                emptyCount = 0
                board.append([])
            elif s in "0123456789":
                emptyCount = emptyCount * 10 + int(s)
            elif s == "+":
                promoteFlag = True
            elif s in "plnsgbrkPLNSGBRK":
                if emptyCount > 0:
                    board[-1].extend(["___"] * emptyCount)
                    emptyCount = 0
                if promoteFlag:
                    if s.islower():
                        board[-1].append(f"w+{s}")
                    else:
                        board[-1].append(f"b+{s.lower()}")
                else:
                    if s.islower():
                        board[-1].append(f"w_{s}")
                    else:
                        board[-1].append(f"b_{s.lower()}")
        elif now == 1:
            if s == " ":
                now += 1
            elif s == "b":
                turn = 1
            elif s == "w":
                turn = 0
        elif now == 2:
            if s == " ":
                now += 1
            elif s in "0123456789":
                handCount = handCount * 10 + int(s)
            elif s in "plnsgbrPLNSGBR":
                if s.islower():
                    if handCount == 0:
                        hand[0]["plnsgbr".find(s)] = 1
                    else:
                        hand[0]["plnsgbr".find(s)] = handCount
                    handCount = 0
                else:
                    if handCount == 0:
                        hand[1]["PLNSGBR".find(s)] = 1
                    else:
                        hand[1]["PLNSGBR".find(s)] = handCount
                    handCount = 0
        elif now == 3:
            if s in "0123456789":
                moves = moves * 10 + int(s)
    return board, turn, hand, moves

def leaperMoves(board, turn, x, y, dx, dy):
    newMoves = []
    if turn == 1:
        x1, y1 = x + dx, y + dy
    else:
        x1, y1 = x - dx, y - dy
    if (0 <= x1 < 9) and (0 <= y1 < 9):
        if board[y1][x1] == "___" or (turn == 1 and board[y1][x1][0] == "w") or (turn == 0 and board[y1][x1][0] == "b"):
            newMoves.append((x, y, x1, y1, 0))
            if (not (board[x][y][1] == "+" or board[x][y][2] in "gk")) and (turn == 1 and (y < 3 or y1 < 3)) or (turn == 0 and (y >= 6 or y1 >= 6)):
                newMoves.append((x, y, x1, y1, 1))
    return newMoves

def riderMoves(board, turn, x, y, dx, dy):
    newMoves = []
    if turn == 1:
        x1, y1 = x + dx, y + dy
    else:
        x1, y1 = x - dx, y - dy
    if (0 <= x1 < 9) and (0 <= y1 < 9):
        while board[y1][x1] == "___":
            newMoves.append((x, y, x1, y1, 0))
            if (not (board[x][y][1] == "+" or board[x][y][2] in "gk")) and (turn == 1 and (y < 3 or y1 < 3)) or (turn == 0 and (y >= 6 or y1 >= 6)):
                newMoves.append((x, y, x1, y1, 1))
            if turn == 1:
                x1 += dx
                y1 += dy
            else:
                x1 -= dx
                y1 -= dy
            if not (0 <= x1 < 9 and 0 <= y1 < 9):
                break
        else:
            if board[y1][x1] == "___" or (turn == 1 and board[y1][x1][0] == "w") or (turn == 0 and board[y1][x1][0] == "b"):
                newMoves.append((x, y, x1, y1, 0))
                if (not (board[x][y][1] == "+" or board[x][y][2] in "gk")) and (turn == 1 and (y < 3 or y1 < 3)) or (turn == 0 and (y >= 6 or y1 >= 6)):
                    newMoves.append((x, y, x1, y1, 1))
    return newMoves

def dropMoves(board, turn, hand):
    newMoves = []
    for y in range(9):
        for x in range(9):
            if board[y][x] == "___":
                for i in range(7):
                    if hand[turn][i] > 0 and not ((turn == 1 and (((i == 0 or i == 1 or i == 2) and y == 0) or (i == 2 and y == 1))) or (turn == 0 and (((i == 0 or i == 1 or i == 2) and y == 8) or (i == 2 and y == 7)))):
                        newMoves.append((9, i, x, y, 0))
    return newMoves

def generateMoves(board, turn, hand, flag=True):
    legalMoves = set()
    for y in range(9):
        for x in range(9):
            if (turn == 1 and board[y][x][0] == "b") or (turn == 0 and board[y][x][0] == "w"):
                for dx, dy, mode in piecesMove[board[y][x][1:]]:
                    if dx == dy == mode == 0:
                        continue
                    elif mode == 0:
                        for i in leaperMoves(board, turn, x, y, dx, dy):
                            legalMoves.add(i)
                    elif mode == 1:
                        for i in riderMoves(board, turn, x, y, dx, dy):
                            legalMoves.add(i)
    if flag:
        illegalMoves = []
        for i in legalMoves:
            winner, _ = makeMoves(copy.deepcopy(board), turn, copy.deepcopy(hand), [i])
            if winner[1 - turn] or CheckCheck(board, turn):
                illegalMoves.append(i)
        for i in illegalMoves:
            legalMoves.remove(i)
    legalMoves = list(legalMoves)
    if flag:
        legalMoves.extend(dropMoves(board, turn, hand))
    return sorted(legalMoves)

def makeMoves(board, turn, hand, useMoves):
    winner = [0, 0]
    for x, y, x1, y1, promoteFlag in useMoves:
        if turn == 1:
            if x == 9:
                board[y1][x1] = f"b_{"plnsgbr"[y]}"
                hand[1][y] -= 1
            else:
                if board[y1][x1] == "___":
                    if promoteFlag:
                        board[y1][x1] = f"b+{board[y][x][2]}"
                    else:
                        board[y1][x1] = f"b{board[y][x][1:]}"
                else:
                    winFlag = explosion(board, turn, hand, x1, y1)
                    if winner[0] == winner[1] == 0:
                        for i in winFlag:
                            winner[i] = 1
                board[y][x] = "___"
        else:
            if x == 9:
                board[y1][x1] = f"w_{"plnsgbr"[y]}"
                hand[0][y] -= 1
            else:
                if board[y1][x1] == "___":
                    if promoteFlag:
                        board[y1][x1] = f"w+{board[y][x][2]}"
                    else:
                        board[y1][x1] = f"w{board[y][x][1:]}"
                else:
                    winFlag = explosion(board, turn, hand, x1, y1)
                    if winner[0] == winner[1] == 0:
                        for i in winFlag:
                            winner[i] = 1
                board[y][x] = "___"
        turn = 1 - turn
    return winner, turn

def explosion(board, turn, hand, x1, y1):
    winFlag = []
    for y in range(y1-1, y1+2):
        for x in range(x1-1, x1+2):
            if (0 <= x < 9 and 0 <= y < 9) and ((x == x1 and y == y1) or board[y][x][1:] != "_p"):
                if board[y][x] == "b_k":
                    winFlag.append(0)
                elif board[y][x] == "w_k":
                    winFlag.append(1)
                elif (turn == 1 and board[y][x][0] == "w") or (turn == 0 and board[y][x][0] == "b"):
                    hand[turn]["plnsgbr".find(board[y][x][2])] += 1
                board[y][x] = "___"
    return winFlag

def CheckCheck(board, turn):
    legalMoves = generateMoves(board, 1 - turn, None, False)
    for i in legalMoves:
        winner, _ = makeMoves(copy.deepcopy(board), 1 - turn, [[0] * 7, [0] * 7], [i])
        if winner[1 - turn]:
            return True
    return False