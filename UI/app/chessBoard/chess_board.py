

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