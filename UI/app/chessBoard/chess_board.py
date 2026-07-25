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


class MakeMoves:

    rankToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRank = {"7":"1", "6":"2", "5":"3", "4":"4", "3":"5", "2":"6", "1":"7", "0":"8"}
    fileToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFile = {"0":"a", "1":"b", "2":"c", "3":"d", "4":"e", "5":"f", "6":"g", "7":"h"}

    def __init__(self,startpos, endpos, board):
        self.startRow = startpos[0]
        self.startCol = startpos[1]
        self.endRow = endpos[0]
        self.endCol = endpos[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]