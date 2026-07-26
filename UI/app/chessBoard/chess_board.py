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

        self.promotionListBlack = [["bR"], ["bN"], ["bB"], ["bQ"]]
        self.promotionListWhite = [["wR"], ["wN"], ["wB"], ["wQ"]]
        
        self.whiteToMove = True
        self.moveLogs = []
        self.blackpieces = ["bR" , "bN", "bB", "bQ", "bK", "bp"]
        self.whitepieces = ["wR" , "wN", "wB", "wQ", "wK", "wp"]
        self.hasWhiteRooksMoved = [False, False]
        self.hasBlackRooksMoved = [False, False]
        self.hasBlackKingMoved = False
        self.hasWhiteKingMoved = False

    def makeMove(self, move):
        validMove = ((move.pieceMoved in ("bp", "wp") and self.pawnMove(move)) or
                    (move.pieceMoved in ("bK", "wK") and self.kingMove(move)) or
                    (move.pieceMoved in ("bQ", "wQ") and self.queenMove(move)) or
                    (move.pieceMoved in ("bN", "wN") and self.nightMove(move)) or
                    (move.pieceMoved in ("bB", "wB") and self.bishopMove(move)) or
                    (move.pieceMoved in ("bR", "wR") and self.rookMove(move)))
        if self.validateTurn(move) and validMove:
            self.board[move.startRow][move.startCol] = "__"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLogs.append(move)  # log the move so we can undo it later
            self.whiteToMove = not self.whiteToMove  # swap players
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
                          
    def pawnMove(self, move):
        if self.validMove(move):
            if (move.pieceMoved == "bp"):
                if move.startRow == 1 and move.endCol == move.startCol and move.endRow == 3:
                    return True
                elif move.endCol == move.startCol and move.endRow - move.startRow == 1:
                    return True
            else:
                if move.startRow == 6 and move.endCol == move.startCol and move.endRow == 4:
                    return True
                elif move.endCol == move.startCol and move.startRow - move.endRow == 1:
                    return True

        return False

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
        if self.validMove(move):
            diffcol = abs(move.startCol - move.endCol)
            diffrow = abs(move.startRow - move.endRow)
            if((diffcol == 1 and diffrow == 2) or (diffrow == 1 and diffcol == 2)):
                return True
        return False

    def kingMove(self, move):
        if self.validMove(move) :
            diffcol = abs(move.startCol - move.endCol)
            diffrow = abs(move.startRow - move.endRow)
            if(diffrow == 1 or diffcol == 1):
                if(move.pieceMoved == "bK"): self.hasBlackKingMoved = True
                else: self.hasWhiteKingMoved = True
                return True

        return False
    

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