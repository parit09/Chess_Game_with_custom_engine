import pygame as pyg
from chessBoard import chessBoard


WIDTH = HEIGHT = 512    # Dimensions of the rendered chess board
SQU_WIDTH = SQU_HEIGHT = 64     # Dimensions of each square in the board
BOARD_DIM = 8

BOARD = {}

def loadAssets():
    pieces = ["bp", "bR" , "bN", "bB", "bQ", "bK", "wp" , "wR" , "wN", "wB", "wQ", "wK"]    #List of pieces 
    BOARD[pieces] = pyg.image.load("assets/" + pieces + "png")   #mapping pieces with their respective pngs





