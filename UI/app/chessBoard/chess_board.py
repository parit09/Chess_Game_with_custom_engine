class ChessBoard:
    def __init__(self):
        self.board = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bp","bp","bp","bp","bp","bp","bp","bp"],
                    ["__","__","__","__","__","__","__","__"],
                    ["__","__","__","__","__","__","__","__"],
                    ["__","__","__","__","__","__","__","__"],
                    ["__","__","__","__","__","__","__","__"],
                    ["wp","wp","wp","wp","wp","wp","wp","wp"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        
        self.whiteToMove = True
        self.moveLogs = []
        self.blackpieces = ["bR" , "bN", "bB", "bQ", "bK", "bp"]
        self.whitepieces = ["wR" , "wN", "wB", "wQ", "wK", "wp"]
        self.hasWhiteRooksMoved = [False, False]
        self.hasBlackRooksMoved = [False, False]
        self.hasBlackKingMoved = False
        self.hasWhiteKingMoved = False
        self.whiteKingPos = (7, 4)
        self.blackKingPos = (0, 4)
        self.pendingPromotion = None
        self.gameOver = None
        self.winnerPieces = []

    def makeMove(self, move):
        if self.pendingPromotion is not None:
            return False

        validMove = ((move.pieceMoved in ("bp", "wp") and self.pawnMove(move)) or
                    (move.pieceMoved in ("bK", "wK") and self.kingMove(move)) or
                    (move.pieceMoved in ("bQ", "wQ") and self.queenMove(move)) or
                    (move.pieceMoved in ("bN", "wN") and self.nightMove(move)) or
                    (move.pieceMoved in ("bB", "wB") and self.bishopMove(move)) or
                    (move.pieceMoved in ("bR", "wR") and self.rookMove(move)))

        if self.validateTurn(move) and validMove:
            enPassantMove = self.Enpassant(move)
            self.board[move.startRow][move.startCol] = "__"
            self.board[move.endRow][move.endCol] = move.pieceMoved

            if enPassantMove and self.whiteToMove:
                self.board[move.endRow + 1][move.endCol] = "__"
            elif enPassantMove and not self.whiteToMove:
                self.board[move.endRow - 1][move.endCol] = "__"

            if(self.isKingInCheck()):
                self.board[move.startRow][move.startCol] = move.pieceMoved 
                self.board[move.endRow][move.endCol] = move.pieceCaptured
                return False

            if move.pieceMoved in ("wp", "bp") and self.isPromotionMove(move):
                return self.beginPromotion(move)
            
            self.moveLogs.append(move)  # log the move so we can undo it later
            self.whiteToMove = not self.whiteToMove  # swap players

            if(move.pieceMoved == "bK"):
                if((move.startRow, move.startCol) == (0, 4) and 
                    (self.blackKingPos == (0, 2) or self.blackKingPos == (0, 6)) 
                    and not self.hasBlackKingMoved):
                    if(self.blackKingPos == (0,2) and not self.hasBlackRooksMoved[0]):
                        self.hasBlackRooksMoved[0] = True
                        self.board[0][0] = "__"
                        self.board[0][3] = "bR"
                    elif(self.blackKingPos == (0,6) and not self.hasBlackRooksMoved[1]):
                        self.hasBlackRooksMoved[1] = True
                        self.board[0][7] = "__"
                        self.board[0][5] = "bR"

                self.hasBlackKingMoved = True
            elif(move.pieceMoved == "wK"):
                if((move.startRow, move.startCol) == (7, 4) and 
                    (self.whiteKingPos == (7, 2) or self.whiteKingPos == (7, 6)) 
                    and not self.hasWhiteKingMoved):
                        if(self.whiteKingPos == (7,2) and not self.hasWhiteRooksMoved[0]):
                            self.hasWhiteRooksMoved[0] = True
                            self.board[7][0] = "__"
                            self.board[7][3] = "wR"
                        elif(self.whiteKingPos == (7,6) and not self.hasWhiteRooksMoved[1]):
                            self.hasWhiteRooksMoved[1] = True
                            self.board[7][7] = "__"
                            self.board[7][5] = "wR"
                
                self.hasWhiteKingMoved = True

            if(move.pieceMoved == "bR"):
                if(move.startRow == 0 and move.startCol == 0):
                    self.hasBlackRooksMoved[0] = True
                elif(move.startRow == 0 and move.startCol == 7):
                    self.hasBlackRooksMoved[1] = True
            if(move.pieceMoved == "wR"):
                if(move.startRow == 7 and move.startCol == 0):
                    self.hasWhiteRooksMoved[0] = True
                elif(move.startRow == 7 and move.startCol == 7):
                    self.hasWhiteRooksMoved[1] = True
            
            return True

        return False

    def validateTurn(self, move):
        if(self.whiteToMove and move.pieceMoved in self.whitepieces) or (not self.whiteToMove and move.pieceMoved in self.blackpieces):
            return True
        return False

    def validMove(self, move):
        if((move.pieceCaptured == "__") or
         (self.whiteToMove and move.pieceCaptured not in self.whitepieces) or
         (not self.whiteToMove and move.pieceCaptured not in self.blackpieces)):
            return True
        return False

    
    def isPromotionMove(self, move):
        return ((move.pieceMoved == "wp" and move.endRow == 0) or
                (move.pieceMoved == "bp" and move.endRow == 7))

    def beginPromotion(self, move):
        self.board[move.startRow][move.startCol] = "__"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        self.pendingPromotion = {
            "move": move,
            "color": "w" if move.pieceMoved == "wp" else "b",
        }

        return "promotion"

    def completePromotion(self, promotedPiece):
        if self.pendingPromotion is None:
            return False

        move = self.pendingPromotion["move"]
        self.board[move.endRow][move.endCol] = promotedPiece
        self.moveLogs.append(move)
        self.whiteToMove = not self.whiteToMove
        self.pendingPromotion = None

        return True

    def possibleBishopMoves(self, move):
        possibleMovesList = []
        currRow = move.startRow
        currCol = move.startCol
        dx = [1, -1, 1, -1]
        dy = [-1, -1, 1, 1]

        for i in range (4):
                x, y = currRow + dx[i], currCol + dy[i] 
                while (x < 8 and y < 8 and x > -1 and y > -1):
                    if(self.board[x][y] == "__"):
                        possibleMovesList.append((x,y))
                    else:
                        if(self.whiteToMove):
                            if(self.board[x][y] in self.blackpieces and self.board[x][y] != "bK"):
                                possibleMovesList.append((x,y))
                        else:
                            if(self.board[x][y] in self.whitepieces and self.board[x][y] != "wK"):
                                possibleMovesList.append((x,y))

                        break
                    x = x + dx[i]
                    y = y + dy[i]

        return possibleMovesList

    def possibleKnightMoves(self, move):
        possibleMovesList = []
        currRow = move.startRow
        currCol = move.startCol
        knightMoves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dx, dy in knightMoves:
            x = currRow + dx
            y = currCol + dy

            if 0 <= x < 8 and 0 <= y < 8:
                if self.board[x][y] == "__":
                    possibleMovesList.append((x, y))
                else:
                    if self.whiteToMove:
                        if self.board[x][y] in self.blackpieces and self.board[x][y] != "bK":
                            possibleMovesList.append((x, y))
                    else:
                        if self.board[x][y] in self.whitepieces and self.board[x][y] != "wK":
                            possibleMovesList.append((x, y))

        return possibleMovesList

    def possibleRookMoves(self, move):
        possibleMovesList = []
        currRow = move.startRow
        currCol = move.startCol
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
    
        for i in range (4):
                x, y = currRow + dx[i], currCol + dy[i] 
                while (x < 8 and y < 8 and x > -1 and y > -1):
                    if(self.board[x][y] == "__"):
                        possibleMovesList.append((x,y))
                    else:
                        if(self.whiteToMove):
                            if(self.board[x][y] in self.blackpieces and self.board[x][y] != "bK"):
                                possibleMovesList.append((x,y))
                        else:
                            if(self.board[x][y] in self.whitepieces and self.board[x][y] != "wK"):
                                possibleMovesList.append((x,y))
                                
                        break
                    x = x + dx[i]
                    y = y + dy[i]
    
        return possibleMovesList

    def isSquareSafe(self, row, col):
        enemy = "b" if self.whiteToMove else "w"

        # ---------------- Pawn Threat ----------------
        if self.whiteToMove:
            if row - 1 >= 0:
                if col - 1 >= 0 and self.board[row - 1][col - 1] == "bp":
                    return False
                if col + 1 < 8 and self.board[row - 1][col + 1] == "bp":
                    return False
        else:
            if row + 1 < 8:
                if col - 1 >= 0 and self.board[row + 1][col - 1] == "wp":
                    return False
                if col + 1 < 8 and self.board[row + 1][col + 1] == "wp":
                    return False

        # ---------------- Rook / Queen Threat ----------------
        rookDirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in rookDirs:
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                piece = self.board[x][y]
                if piece != "__":
                    if piece == enemy + "R" or piece == enemy + "Q":
                        return False
                    break

                x += dx
                y += dy

        # ---------------- Bishop / Queen Threat ----------------
        bishopDirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in bishopDirs:
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                piece = self.board[x][y]
                if piece != "__":
                    if piece == enemy + "B" or piece == enemy + "Q":
                        return False
                    break

                x += dx
                y += dy

        # ---------------- Knight Threat ----------------
        knightMoves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dx, dy in knightMoves:
            x = row + dx
            y = col + dy

            if 0 <= x < 8 and 0 <= y < 8:
                if self.board[x][y] == enemy + "N":
                    return False

        # ---------------- King Threat ----------------
        kingMoves = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]

        for dx, dy in kingMoves:
            x = row + dx
            y = col + dy

            if 0 <= x < 8 and 0 <= y < 8:
                if self.board[x][y] == enemy + "K":
                    return False

        return True

    def possiblePawnMoves(self, move):
        possibleMovesList = []
        startRow = move.startRow
        startCol = move.startCol

        if move.pieceMoved == "wp":
            oneStepRow = startRow - 1
            twoStepRow = startRow - 2

            if oneStepRow >= 0 and self.board[oneStepRow][startCol] == "__":
                possibleMovesList.append((oneStepRow, startCol))

                if startRow == 6 and self.board[twoStepRow][startCol] == "__":
                    possibleMovesList.append((twoStepRow, startCol))

            for colOffset in (-1, 1):
                captureCol = startCol + colOffset
                if oneStepRow >= 0 and 0 <= captureCol < 8:
                    targetPiece = self.board[oneStepRow][captureCol]
                    if targetPiece in self.blackpieces and targetPiece != "bK":
                        possibleMovesList.append((oneStepRow, captureCol))

            if self.Enpassant(move):
                possibleMovesList.append((move.endRow, move.endCol))

        else:
            oneStepRow = startRow + 1
            twoStepRow = startRow + 2

            if oneStepRow < 8 and self.board[oneStepRow][startCol] == "__":
                possibleMovesList.append((oneStepRow, startCol))

                if startRow == 1 and self.board[twoStepRow][startCol] == "__":
                    possibleMovesList.append((twoStepRow, startCol))

            for colOffset in (-1, 1):
                captureCol = startCol + colOffset
                if oneStepRow < 8 and 0 <= captureCol < 8:
                    targetPiece = self.board[oneStepRow][captureCol]
                    if targetPiece in self.whitepieces and targetPiece != "wK":
                        possibleMovesList.append((oneStepRow, captureCol))

            if self.Enpassant(move):
                possibleMovesList.append((move.endRow, move.endCol))

        return possibleMovesList
    
    def pawnMove(self, move):
        return self.validMove(move) and (move.endRow, move.endCol) in self.possiblePawnMoves(move)

    def pawnTakes(self, move):
        if(self.whiteToMove and move.pieceCaptured[0] == "b" and move.pieceCaptured[1] != "K"): return True
        elif(not self.whiteToMove and move.pieceCaptured[0] == "w" and move.pieceCaptured[1] != "K"): return True
        elif(self.Enpassant(move)): return True
        return False

    def Enpassant(self, move):
        if len(self.moveLogs) == 0:
            return False

        lastMove = self.moveLogs[-1]

        if self.whiteToMove:
            return (
                move.pieceMoved == "wp" and
                lastMove.pieceMoved == "bp" and
                move.startRow == 3 and
                lastMove.startRow == 1 and
                lastMove.endRow == 3 and
                abs(lastMove.endCol - move.startCol) == 1 and
                move.endRow == 2 and
                move.endCol == lastMove.endCol
            )

        return (
                move.pieceMoved == "bp" and
                lastMove.pieceMoved == "wp" and
                move.startRow == 4 and
                lastMove.startRow == 6 and
                lastMove.endRow == 4 and
                abs(lastMove.endCol - move.startCol) == 1 and
                move.endRow == 5 and
                move.endCol == lastMove.endCol
            )


    def rookMove(self, move):
        if (self.validMove(move) and (move.startRow == move.endRow or move.startCol == move.endCol)
            and (move.endRow, move.endCol) in self.possibleRookMoves(move)):
                return True
        return False

    def bishopMove(self, move):
        if (self.validMove(move) and (abs(move.startRow - move.endRow) == abs(move.startCol - move.endCol))
            and (move.endRow, move.endCol) in self.possibleBishopMoves(move)):
                return True
        return False

    def queenMove(self, move):
        return self.rookMove(move) or self.bishopMove(move)

    def nightMove(self, move):
        if self.validMove(move) and (move.endRow, move.endCol) in self.possibleKnightMoves(move):
            return True
        return False

    def isKingInCheck(self):
        kingPos = self.whiteKingPos if self.whiteToMove else self.blackKingPos
        return not self.isSquareSafe(kingPos[0], kingPos[1])

    def kingMove(self, move):
        if(self.validMove(move) and (move.endRow, move.endCol) in self.possibleKingMoves(move)):
            if move.pieceMoved == "wK":
                self.whiteKingPos = (move.endRow, move.endCol)
            if move.pieceMoved == "bK":
                self.blackKingPos = (move.endRow, move.endCol)

            return True

        return False
    
    def possibleKingMoves(self, move):
        possibleMovesList = []
        currRow = move.startRow
        currCol = move.startCol
        dx = [1, 1, 1, 0, -1, -1, -1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]

        for i in range (8):
                x, y = currRow + dx[i], currCol + dy[i] 
                if (x < 8 and y < 8 and x > -1 and y > -1):
                    if(self.board[x][y] == "__"):
                        if self._isKingMoveSafe(move, x, y):
                            possibleMovesList.append((x,y))
                    else:
                        if(self.whiteToMove):
                            if(self.board[x][y] in self.blackpieces and self.board[x][y] != "bK" and self._isKingMoveSafe(move, x, y)):
                                possibleMovesList.append((x,y))
                        else:
                            if(self.board[x][y] in self.whitepieces and self.board[x][y] != "wK" and self._isKingMoveSafe(move, x, y)):
                                possibleMovesList.append((x,y))

        if(self.isCastlingPossible(move)):
            self.castlingMove(possibleMovesList)

        return possibleMovesList

    def _isKingMoveSafe(self, move, endRow, endCol):
        startRow, startCol = move.startRow, move.startCol
        movingPiece = self.board[startRow][startCol]
        capturedPiece = self.board[endRow][endCol]
        savedWhiteKingPos = self.whiteKingPos
        savedBlackKingPos = self.blackKingPos

        self.board[startRow][startCol] = "__"
        self.board[endRow][endCol] = movingPiece

        if movingPiece == "wK":
            self.whiteKingPos = (endRow, endCol)
        else:
            self.blackKingPos = (endRow, endCol)

        safe = self.isSquareSafe(endRow, endCol)

        self.board[startRow][startCol] = movingPiece
        self.board[endRow][endCol] = capturedPiece
        self.whiteKingPos = savedWhiteKingPos
        self.blackKingPos = savedBlackKingPos

        return safe

    def isCastlingPossible(self, move):
        if(self.whiteToMove and not self.hasWhiteKingMoved and 
           ((not self.hasWhiteRooksMoved[0] and self.board[7][3] == self.board[7][2] == self.board[7][1] == "__") or
            (not self.hasWhiteRooksMoved[1] and self.board[7][5] == self.board[7][6] == "__"))):
            return True
        elif(not self.whiteToMove and not self.hasBlackKingMoved and 
           ((not self.hasBlackRooksMoved[0] and self.board[0][3] == self.board[0][2] == self.board[0][1] == "__") or
            (not self.hasBlackRooksMoved[1] and self.board[0][5] == self.board[0][6] == "__"))):
            return True

        return False

    def castlingMove(self, possibleMovesList):
        if self.whiteToMove:
            if not self.hasWhiteKingMoved:
                # Queenside
                if (not self.hasWhiteRooksMoved[0] and
                    self.board[7][3] == self.board[7][2] == self.board[7][1] == "__" 
                    and (self.isSquareSafe(7, 0) and self.isSquareSafe(7, 1) and self.isSquareSafe(7, 2)
                    and self.isSquareSafe(7, 3) and self.isSquareSafe(7,4))
                    and self.board[7][0] == "wR" and not self.hasWhiteRooksMoved[0]):
                    possibleMovesList.append((7, 2))

                # Kingside
                if (not self.hasWhiteRooksMoved[1] and
                    self.board[7][5] == self.board[7][6] == "__" 
                    and (self.isSquareSafe(7, 4) and self.isSquareSafe(7, 5) 
                    and self.isSquareSafe(7, 6) and self.isSquareSafe(7, 7))
                    and self.board[7][7] == "wR" and not self.hasWhiteRooksMoved[1]):
                    possibleMovesList.append((7, 6))

        else:
            if not self.hasBlackKingMoved:
                # Queenside
                if (not self.hasBlackRooksMoved[0] and
                    self.board[0][3] == self.board[0][2] == self.board[0][1] == "__"
                    and (self.isSquareSafe(0, 0) and self.isSquareSafe(0, 1) and self.isSquareSafe(0, 2)
                    and self.isSquareSafe(0, 3) and self.isSquareSafe(0,4))
                    and self.board[0][0] == "bR" and not self.hasBlackRooksMoved[0]):
                    possibleMovesList.append((0, 2))

                # Kingside
                if (not self.hasBlackRooksMoved[1] and
                    self.board[0][5] == self.board[0][6] == "__"
                    and (self.isSquareSafe(0, 4) and self.isSquareSafe(0, 5) 
                    and self.isSquareSafe(0, 6) and self.isSquareSafe(0, 7))
                    and self.board[0][7] == "bR" and not self.hasBlackRooksMoved[1]):
                    possibleMovesList.append((0, 6))

    def validPieceMove(self, move, possibleMoves=None):
        if possibleMoves is None:
            if move.pieceMoved in ("bp", "wp"):
                possibleMoves = self.possiblePawnMoves(move)
            elif move.pieceMoved in ("bR", "wR"):
                possibleMoves = self.possibleRookMoves(move)
            elif move.pieceMoved in ("bN", "wN"):
                possibleMoves = self.possibleKnightMoves(move)
            elif move.pieceMoved in ("bB", "wB"):
                possibleMoves = self.possibleBishopMoves(move)
            elif move.pieceMoved in ("bQ", "wQ"):
                possibleMoves = self.possibleRookMoves(move) + self.possibleBishopMoves(move)
            elif move.pieceMoved in ("bK", "wK"):
                possibleMoves = self.possibleKingMoves(move)
            else:
                return []

        if move.pieceMoved in ("bK", "wK"):
            return [candidate for candidate in possibleMoves if self._isKingMoveSafe(move, candidate[0], candidate[1])]

        return possibleMoves

    def validPieceMoves(self, move):
        return self.validPieceMove(move)

    def hasAnyLegalMoves(self):
        from .chess_board import MakeMoves as _MM  # local reference (safe at runtime)
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == "__":
                    continue
                if (self.whiteToMove and piece[0] != 'w') or (not self.whiteToMove and piece[0] != 'b'):
                    continue

                start = (r, c)
                probe = _MM(start, start, self.board)
                candidates = self.validPieceMoves(probe)
                for dest in candidates:
                    endR, endC = dest
                    movedPiece = self.board[r][c]
                    captured = self.board[endR][endC]

                    # make the move on board temporarily
                    self.board[r][c] = "__"
                    self.board[endR][endC] = movedPiece
                    savedWhite = self.whiteKingPos
                    savedBlack = self.blackKingPos
                    if movedPiece == "wK":
                        self.whiteKingPos = (endR, endC)
                    elif movedPiece == "bK":
                        self.blackKingPos = (endR, endC)

                    inCheck = self.isKingInCheck()

                    # restore
                    self.board[r][c] = movedPiece
                    self.board[endR][endC] = captured
                    self.whiteKingPos = savedWhite
                    self.blackKingPos = savedBlack

                    if not inCheck:
                        return True

        return False

    def isCheckmate(self):
        return self.isKingInCheck() and not self.hasAnyLegalMoves()

    def isStalemate(self):
        return (not self.isKingInCheck()) and (not self.hasAnyLegalMoves())

    def getWinnerPieces(self):
        # return list of remaining pieces for the side that is NOT to move (the player who just moved)
        winner_color = 'w' if not self.whiteToMove else 'b'
        pieces = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != "__" and p[0] == winner_color:
                    pieces.append(p)
        return pieces

    

class MakeMoves:

    rankToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRank = {v:k for k, v in rankToRows.items()}
    fileToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFile = {v:k for k, v in fileToCols.items()}

    def __init__(self,startpos, endpos, board):
        self.startRow = startpos[0]
        self.startCol = startpos[1]
        self.endRow = endpos[0]
        self.endCol = endpos[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFile[c] + self.rowsToRank[r]