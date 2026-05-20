import copy, random, time

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
                if emptyCount > 0:
                    board[-1].extend(["___"] * emptyCount)
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
            if (not (board[y][x][1] == "+" or board[y][x][2] in "gk")) and (turn == 1 and (y < 3 or y1 < 3)) or (turn == 0 and (y >= 6 or y1 >= 6)):
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
            if (not (board[y][x][1] == "+" or board[y][x][2] in "gk")) and (turn == 1 and (y < 3 or y1 < 3)) or (turn == 0 and (y >= 6 or y1 >= 6)):
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
                if (not (board[y][x][1] == "+" or board[y][x][2] in "gk")) and (turn == 1 and (y < 3 or y1 < 3)) or (turn == 0 and (y >= 6 or y1 >= 6)):
                    newMoves.append((x, y, x1, y1, 1))
    return newMoves

def dropMoves(board, turn, hand):
    newMoves = []
    for y in range(9):
        for x in range(9):
            if board[y][x] == "___":
                for i in range(7):
                    if hand[turn][i] > 0 and not ((turn == 1 and (((i == 0 or i == 1 or i == 2) and y == 0) or (i == 2 and y == 1))) or (turn == 0 and (((i == 0 or i == 1 or i == 2) and y == 8) or (i == 2 and y == 7)))):
                        if i == 0:
                            for y1 in range(9):
                                if (turn == 1 and board[y1][x] == "b_p") or (turn == 0 and board[y1][x] == "w_p"):
                                    break
                            else:
                                newMoves.append((9, i, x, y, 0))
                        else:
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
        legalMoves |= set(dropMoves(board, turn, hand))
        illegalMoves = []
        for i in legalMoves:
            winner, _, delta = makeMoves(board, turn, [[0] * 7, [0] * 7], [i])
            if winner[1 - turn] or CheckCheck(board, turn):
                illegalMoves.append(i)
            undo(board, turn, [[0] * 7, [0] * 7], delta)
        for i in illegalMoves:
            legalMoves.remove(i)
    legalMoves = list(legalMoves)
    return sorted(legalMoves)

def makeMoves(board, turn, hand, useMoves):
    winner = [0, 0]
    delta = {"add": [], "remove": [], "hand": []}
    for x, y, x1, y1, promoteFlag in useMoves:
        if turn == 1:
            if x == 9:
                board[y1][x1] = f"b_{'plnsgbr'[y]}"
                delta["add"].append((x1, y1, board[y1][x1]))
                hand[1][y] -= 1
                delta["hand"].append((1, y, -1))
            else:
                if board[y1][x1] == "___":
                    if promoteFlag:
                        board[y1][x1] = f"b+{board[y][x][2]}"
                    else:
                        board[y1][x1] = f"b{board[y][x][1:]}"
                    delta["add"].append((x1, y1, board[y1][x1]))
                    delta["remove"].append((x, y, board[y][x]))
                else:
                    delta["remove"].append((x, y, board[y][x]))
                    winFlag = explosion(board, turn, hand, x1, y1, delta)
                    if winner[0] == winner[1] == 0:
                        for i in winFlag:
                            winner[i] = 1
                board[y][x] = "___"
        else:
            if x == 9:
                board[y1][x1] = f"w_{'plnsgbr'[y]}"
                delta["add"].append((x1, y1, board[y1][x1]))
                hand[0][y] -= 1
                delta["hand"].append((1, y, -1))
            else:
                if board[y1][x1] == "___":
                    if promoteFlag:
                        board[y1][x1] = f"w+{board[y][x][2]}"
                    else:
                        board[y1][x1] = f"w{board[y][x][1:]}"
                    delta["add"].append((x1, y1, board[y1][x1]))
                    delta["remove"].append((x, y, board[y][x]))
                else:
                    delta["remove"].append((x, y, board[y][x]))
                    winFlag = explosion(board, turn, hand, x1, y1, delta)
                    if winner[0] == winner[1] == 0:
                        for i in winFlag:
                            winner[i] = 1
                board[y][x] = "___"
        turn = 1 - turn
    return winner, turn, delta

def explosion(board, turn, hand, x1, y1, delta):
    winFlag = []
    for y in range(y1-1, y1+2):
        for x in range(x1-1, x1+2):
            if (0 <= x < 9 and 0 <= y < 9) and ((x == x1 and y == y1) or board[y][x][1:] != "_p"):
                delta["remove"].append((x, y, board[y][x]))
                if board[y][x] == "b_k":
                    winFlag.append(0)
                elif board[y][x] == "w_k":
                    winFlag.append(1)
                elif (turn == 1 and board[y][x][0] == "w") or (turn == 0 and board[y][x][0] == "b"):
                    hand[turn]["plnsgbr".find(board[y][x][2])] += 1
                    delta["hand"].append((turn, "plnsgbr".find(board[y][x][2]), 1))
                board[y][x] = "___"
    return winFlag

def CheckCheck(board, turn):
    legalMoves = generateMoves(board, 1 - turn, None, False)
    for i in legalMoves:
        winner, _, delta = makeMoves(board, 1 - turn, [[0] * 7, [0] * 7], [i])
        #print(delta)
        undo(board, turn, [[0] * 7, [0] * 7], delta)
        if winner[1 - turn]:
            return True
    return False

def df_pn(board, turn, hand, StartTurn, HASH, node, table={0:{"pn": 1, "dn": 1, "depth": -1, "isLeaf": True, "mateMove": []}}, depth=0, thpn=1, thdn=1, move=[], incFlag=True, timeLimit=float("inf"), startTime=time.time()):
    if table[HASH.hashNum]["isLeaf"]:
        node[0] += 1
    legalMoves = generateMoves(board, turn, hand)
    MovesWithCheck = [] # 詰将棋として合法な手
    for i in legalMoves:
        delta = positionDelta(board, turn, hand, i)
        _, _, delta1 = makeMoves(board, turn, hand, [i])
        HASH.toggleHash(delta)
        if turn == StartTurn:
            if CheckCheck(board, 1 - turn):
                if HASH.hashNum in table and table[HASH.hashNum]["depth"] < depth:
                    pass
                else:
                    MovesWithCheck.append(i)
        else:
            MovesWithCheck.append(i)
        HASH.toggleHash(delta)
        undo(board, turn, hand, delta1)
    if len(MovesWithCheck) == 0:
        if turn == StartTurn:
            table[HASH.hashNum]["pn"] = float("inf")
            table[HASH.hashNum]["dn"] = 0
        else:
            table[HASH.hashNum]["pn"] = 0
            table[HASH.hashNum]["dn"] = float("inf")
            table[HASH.hashNum]["mateMove"] = copy.deepcopy(move)
        return
    firstFlag = True
    while True:
        if time.time() - startTime >= timeLimit:
            return
        if table[HASH.hashNum]["isLeaf"]:
            incFlag = False
        if turn == StartTurn:
            pn, dn = float("inf"), 0
        else:
            pn, dn = 0, float("inf")
        pnList, dnList = [], []
        mateMove = [None] * 2000
        for i in MovesWithCheck:
            delta = positionDelta(board, turn, hand, i)
            HASH.toggleHash(delta)
            if HASH.hashNum in table:
                if table[HASH.hashNum]["dn"] == float("inf") and len(mateMove) > len(table[HASH.hashNum]["mateMove"]):
                    mateMove = copy.deepcopy(table[HASH.hashNum]["mateMove"])
                if turn == StartTurn:
                    pn = min(pn, table[HASH.hashNum]["pn"])
                    dn += table[HASH.hashNum]["dn"]
                else:
                    pn += table[HASH.hashNum]["pn"]
                    dn = min(dn, table[HASH.hashNum]["dn"])
            else:
                table[HASH.hashNum] = {
                    "pn": 1,
                    "dn": 1,
                    "depth": depth,
                    "isLeaf": True,
                    "mateMove": []
                }
                if turn == StartTurn:
                    pn = min(pn, 1)
                    dn += 1
                else:
                    pn += 1
                    dn = min(dn, 1)
            if turn == StartTurn:
                pnList.append((table[HASH.hashNum]["pn"], i, HASH.hashNum))
            else:
                dnList.append((table[HASH.hashNum]["dn"], i, HASH.hashNum))
            HASH.toggleHash(delta)
        table[HASH.hashNum]["pn"] = pn
        table[HASH.hashNum]["dn"] = dn
        if pn == float("inf") or dn == float("inf"):
            if dn == float("inf"):
                table[HASH.hashNum]["mateMove"] = mateMove
            if depth == 0:
                return table[HASH.hashNum]["mateMove"]
            else:
                return
        if firstFlag and incFlag:
            thpn, thdn = max(thpn, pn + 1), max(thdn, dn + 1)
        table[HASH.hashNum]["isLeaf"] = False
        if (pn >= thpn or dn >= thdn) and depth > 0:
            return
        if turn == StartTurn:
            pnList.sort()
            if len(pnList) == 1:
                Min1, Min2 = pnList[0], pnList[0]
            else:
                Min1, Min2 = pnList[0], pnList[1]
            childThpn = min(thpn, table[Min2[2]]["pn"] + 1)
            childThdn = thdn - dn + table[Min2[2]]["dn"]
        else:
            dnList.sort()
            if len(dnList) == 1:
                Min1, Min2 = dnList[0], dnList[0]
            else:
                Min1, Min2 = dnList[0], dnList[1]
            childThpn = thpn - pn + table[Min2[2]]["pn"]
            childThdn = min(thdn, table[Min2[2]]["dn"] + 1)
        delta = positionDelta(board, turn, hand, Min1[1])
        _, _, delta1 = makeMoves(board, turn, hand, [Min1[1]])
        HASH.toggleHash(delta)
        move.append(Min1[1])
        df_pn(board, 1 - turn, hand, StartTurn, HASH, node, table, depth + 1, childThpn, childThdn, move, timeLimit=timeLimit, startTime=startTime)
        move.pop()
        HASH.toggleHash(delta)
        undo(board, turn, hand, delta1)

def positionDelta(board, turn, hand, useMove):
    delta = []
    const1 = [0, 18, 22, 26, 30, 34, 36]
    const2 = ["_p", "_l", "_n", "_s", "_g", "_b", "_r", "_k", "+p", "+l", "+n", "+s", "+b", "+r"]
    x, y, x1, y1, promoteFlag = useMove
    if x == 9:
        delta.append(turn * 14 + y + y1 * 28 + x1 * 252)
        delta.append(2268 + const1[y] + hand[turn][y] - 1 + turn * 38)
        if hand[turn][y] != 1:
            delta.append(2268 + const1[y] + hand[turn][y] - 2 + turn * 38)
    else:
        delta.append(const2.index(board[y][x][1:]) + turn * 14 + y * 28 + x * 252)
        if board[y1][x1] == "___":
            if promoteFlag or board[y][x][1] == "+":
                delta.append("plnsbr".index(board[y][x][2]) + 8 + turn * 14 + y1 * 28 + x1 * 252)
            else:
                delta.append("plnsgbrk".index(board[y][x][2]) + turn * 14 + y1 * 28 + x1 * 252)
        else:
            for y2 in range(y1-1, y1+2):
                for x2 in range(x1-1, x1+2):
                    if (0 <= y2 < 9 and 0 <= x2 < 9) and (board[y2][x2] != "___"):
                        if (board[y2][x2][0] == "b" and turn == 0) or (board[y2][x2][0] == "w" and turn == 1):
                            if hand[turn]["plnsgbr".index(board[y2][x2][2])] != 0:
                                delta.append(2268 + hand[turn]["plnsgbr".index(board[y2][x2][2])] - 1 + turn * 38)
                            delta.append(2268 + hand[turn]["plnsgbr".index(board[y2][x2][2])] + turn * 38)
                        delta.append(const2.index(board[y2][x2][1:]) + (board[y2][x2][0] == "b") * 14 + y2 * 28 + x2 * 252)
    delta.append(2344)
    return delta

def undo(board, turn, hand, delta):
    for x, y, piece in delta["add"]:
        board[y][x] = "___"
    for x, y, piece in delta["remove"]:
        board[y][x] = piece
    for t, num, d in delta["hand"]:
        hand[t][num] -= d

def negaalpha(board, turn, hand, depth, alpha=-float("inf"), beta=float("inf"), timeLimit=float("inf"), startTime=time.time()):
    if depth <= 0:
        return Ev(board, turn, hand), None
    legalMoves = generateMoves(board, turn, hand)
    if len(legalMoves) == 0:
        return -float("inf"), None
    maxScore = -float("inf")
    maxMove = None
    for move in legalMoves:
        _, _, delta = makeMoves(board, turn, hand, [move])
        moveScore, _ = negaalpha(board, 1 - turn, hand, depth - 1, -beta, -alpha, timeLimit=timeLimit, startTime=startTime)
        moveScore *= -1
        undo(board, turn, hand, delta)
        if maxScore < moveScore:
            maxMove = move
            maxScore = moveScore
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break
    return maxScore, maxMove

def Ev(board, turn, hand):
    piecesScore = {
        "_p": 100,
        "_l": 250,
        "_n": 400,
        "_s": 425,
        "_g": 450,
        "_b": 700,
        "_r": 750,
        "_k": 1000000,
        "+p": 550,
        "+l": 525,
        "+n": 500,
        "+s": 475,
        "+b": 900,
        "+r": 1000
    }
    score = 0
    kings = {"b": (-1, -1), "w": (-1, -1)}
    for x in range(9):
        for y in range(9):
            if board[y][x][2] == "k":
                kings[board[y][x][0]] = (x, y)
    for x in range(9):
        for y in range(9):
            if board[y][x] != "___" and board[y][x][2] != "k":
                if (turn == 0 and board[y][x][0] == "w") or (turn == 1 and board[y][x][0] == "b"):
                    score += piecesScore[board[y][x][1:]] * (1 + 2 * (min(abs(x - kings["bw"[turn]][0]), abs(y - kings["bw"[turn]][1])) == 1))
                else:
                    score -= piecesScore[board[y][x][1:]] * (1 + 2 * (min(abs(x - kings["wb"[turn]][0]), abs(y - kings["wb"[turn]][1])) == 1))
    const2 = ["_p", "_l", "_n", "_s", "_g", "_b", "_r"]
    for i in range(7):
        score += piecesScore[const2[i]] * hand[turn][i] * 2
    for i in range(7):
        score -= piecesScore[const2[i]] * hand[1 - turn][i] * 2
    return score

def ASthoomgiic(board, turn, hand, limit=10.0):
    HASH = Zobrist()
    ans = df_pn(board, turn, hand, turn, HASH, [0], timeLimit=limit / 5)
    if ans is not None:
        return float("inf"), ans[0]
    score, move = negaalpha(board, turn, hand, depth=2, timeLimit=limit / 4 * 3)
    return score, move

class Zobrist:
    def __init__(self):
        self.hashNum = 0
        self.toHashNum = [random.getrandbits(64) for i in range(2345)]
        # 0~2267: Board
        # 2268~2343: Hand
        # 2344: Turn
    def toggleHash(self, d):
        for i in d:
            self.hashNum ^= self.toHashNum[i]
