from pathlib import Path

import pygame as pyg

from chessBoard.chess_board import ChessBoard, MakeMoves


WIDTH = HEIGHT = 512    # Dimensions of the rendered chess board
SQU_WIDTH = SQU_HEIGHT = 64     # Dimensions of each square in the board
DIM = 8
MAX_FPS = 60

BOARD = {}
PROMOTION_CHOICES = {
    "w": ["wR", "wN", "wB", "wQ"],
    "b": ["bR", "bN", "bB", "bQ"],
}


def isSelectablePiece(gamestate, row, col):
    piece = gamestate.board[row][col]
    if piece == "__":
        return False
    if gamestate.whiteToMove:
        return piece in gamestate.whitepieces
    return piece in gamestate.blackpieces

def loadAssets():
    pieces = ["bp", "bR" , "bN", "bB", "bQ", "bK", "wp" , "wR" , "wN", "wB", "wQ", "wK"]    #List of pieces 
    for piece in pieces:
        BOARD[piece] = pyg.image.load("assets/" + f"{piece}.png")   #mapping pieces with their respective pngs


def getPromotionPanelRect(gamestate):
    promotion = gamestate.pendingPromotion
    if promotion is None:
        return None

    move = promotion["move"]
    panel_width = SQU_WIDTH
    panel_height = 4 * SQU_HEIGHT

    x = move.endCol * SQU_WIDTH
    if x + panel_width > WIDTH:
        x = WIDTH - panel_width

    if promotion["color"] == "w":
        y = (move.endRow + 1) * SQU_HEIGHT
    else:
        y = (move.endRow * SQU_HEIGHT) - panel_height

    y = max(0, min(y, HEIGHT - panel_height))
    return pyg.Rect(x, y, panel_width, panel_height)


def handlePromotionClick(gamestate, location):
    panelRect = getPromotionPanelRect(gamestate)
    if panelRect is None or not panelRect.collidepoint(location):
        return False

    promotion = gamestate.pendingPromotion
    optionIndex = (location[1] - panelRect.top) // SQU_HEIGHT
    if 0 <= optionIndex < 4:
        promotedPiece = PROMOTION_CHOICES[promotion["color"]][optionIndex]
        gamestate.completePromotion(promotedPiece)

    return True



def main():
    pyg.init()
    screen = pyg.display.set_mode((WIDTH, HEIGHT))
    clock = pyg.time.Clock()
    gamestate = ChessBoard()
    loadAssets()

    running = True
    squareSelected = ()  # keeps track of the last square clicked (row, col)
    squareClicked = []  # keeps track of the last two squares clicked (two tuples)

    while running:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False
            elif event.type == pyg.MOUSEBUTTONDOWN:
                location = pyg.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQU_WIDTH
                row = location[1] // SQU_HEIGHT
                print((row, col))

                if gamestate.pendingPromotion is not None:
                    handlePromotionClick(gamestate, location)
                    continue

                if squareSelected == (row, col):  # the user clicked the same square twice
                    squareSelected = ()  # deselect
                    squareClicked = []  # clear clicks
                elif not squareClicked:
                    if isSelectablePiece(gamestate, row, col):
                        squareSelected = (row, col)
                        squareClicked.append(squareSelected)
                else:
                    squareSelected = (row, col)
                    squareClicked.append(squareSelected)  # append for both 1st and 2nd clicks

                if len(squareClicked) == 2:  # after 2nd click
                    move = MakeMoves(squareClicked[0], squareClicked[1], gamestate.board)
                    print(move.getChessNotation())
                    gamestate.makeMove(move)
                    squareSelected = ()  # reset user clicks
                    squareClicked = []
        
        drawGameState(screen, gamestate, squareSelected)
        clock.tick(MAX_FPS)
        pyg.display.flip()


def drawGameState(screen, gamestate, squareSelected=()):
    drawBoard(screen)
    validMoves = []
    if squareSelected != ():
        selectedMove = MakeMoves(squareSelected, squareSelected, gamestate.board)
        validMoves = gamestate.validPieceMoves(selectedMove)

    hilightSquare(screen, gamestate, validMoves, squareSelected=squareSelected)
    drawPieces(screen, gamestate.board)
    drawPromotionDropdown(screen, gamestate)


def drawBoard(screen):
    global colors
    colors = [pyg.Color("white"), pyg.Color("gray")]
    for r in range(DIM):
        for c in range(DIM):
            color = colors[((r+c) % 2)]
            pyg.draw.rect(screen, color, pyg.Rect(c*SQU_WIDTH, r*SQU_HEIGHT, SQU_WIDTH, SQU_HEIGHT))

def drawPieces(screen, board):
    for r in range(DIM):
        for c in range(DIM):
            piece = board[r][c]
            if piece != "__":
                screen.blit(BOARD[piece], pyg.Rect(c*SQU_WIDTH, r*SQU_HEIGHT, SQU_WIDTH, SQU_HEIGHT))


def drawPromotionDropdown(screen, gamestate):
    panelRect = getPromotionPanelRect(gamestate)
    if panelRect is None:
        return

    promotion = gamestate.pendingPromotion
    bgColor = pyg.Color("dodgerblue") if promotion["color"] == "w" else pyg.Color("saddlebrown")
    borderColor = pyg.Color("black")
    optionColor = pyg.Color(255, 255, 255, 40)

    pyg.draw.rect(screen, bgColor, panelRect)
    pyg.draw.rect(screen, borderColor, panelRect, 2)

    pieces = PROMOTION_CHOICES[promotion["color"]]
    for index, piece in enumerate(pieces):
        optionRect = pyg.Rect(panelRect.x, panelRect.y + index * SQU_HEIGHT, SQU_WIDTH, SQU_HEIGHT)
        pyg.draw.rect(screen, optionColor, optionRect, 1)
        screen.blit(BOARD[piece], optionRect)

def hilightSquare(screen, gamestate, validMoves, squareSelected):
    if(squareSelected != ()):
        r, c = squareSelected
        if gamestate.board[r][c][0] == ("w" if gamestate.whiteToMove else "b"):
            s = pyg.Surface((SQU_WIDTH, SQU_HEIGHT))
            s.set_alpha(100)  # transparency value
            s.fill(pyg.Color("purple"))
            screen.blit(s, (c*SQU_WIDTH, r*SQU_HEIGHT))

            s.fill(pyg.Color("blue"))
            for move in validMoves:
                endRow, endCol = move
                screen.blit(s, (endCol*SQU_WIDTH, endRow*SQU_HEIGHT))

# animating the move

def animateMove(move, screen, gamestate, clock):
    global colors
    coordinates = []
    dR = move.endrow - move.startRow
    dC = move.endCol - move.startCol
    framespersquare = 10 # frames moved per square
    framescount = framespersquare * (abs(dR) + abs(dC))
    for frame in range(framescount + 1):
        coordinates.append((move.startRow + dR * frame/framescount, move.startCol + dC * frame/framescount)) 


if __name__ == "__main__":
    main()



