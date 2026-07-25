from pathlib import Path

import pygame as pyg

from chessBoard.chess_board import ChessBoard


WIDTH = HEIGHT = 512    # Dimensions of the rendered chess board
SQU_WIDTH = SQU_HEIGHT = 64     # Dimensions of each square in the board
DIM = 8
MAX_FPS = 60

BOARD = {}

def loadAssets():
    pieces = ["bp", "bR" , "bN", "bB", "bQ", "bK", "wp" , "wR" , "wN", "wB", "wQ", "wK"]    #List of pieces 
    for piece in pieces:
        BOARD[piece] = pyg.image.load("assets/" + f"{piece}.png")   #mapping pieces with their respective pngs



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
                print(row, col)

                if squareSelected == (row, col):  # the user clicked the same square twice
                    squareSelected = ()  # deselect
                    squareClicked = []  # clear clicks
                else:
                    squareSelected = (row, col)
                    squareClicked.append(squareSelected)  # append for both 1st and 2nd clicks
        
        drawGameState(screen, gamestate)
        clock.tick(MAX_FPS)
        pyg.display.flip()


def drawGameState(screen, gamestate):
    drawBoard(screen)
    drawPieces(screen, gamestate.board)


def drawBoard(screen):
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

if __name__ == "__main__":
    main()



