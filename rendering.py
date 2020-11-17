import sys, pygame
import pygame.freetype
import berserk
import threading
from game import Game
from queue import Queue
from piece import Piece
from pygame.locals import *
from square import Square
from client import EventStream
from client import GameStream

session = berserk.TokenSession('V4lt6pmQmgrbzgIB')
client = berserk.Client(session)

is_polite = True

gameId = "nYnr74vr"

moves = []

pygame.init()

SCREENWIDTH = 1024 #1920
SCREENHEIGHT = 600 #1080
XBUFFER = (SCREENWIDTH - SCREENHEIGHT) / 2

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
SCREEN.fill((0, 0, 0))

squares = {}
pieces = {}


myfont = pygame.freetype.SysFont('Verdana', 30)

filename = 'assets/pieces.png'
pieces_image = pygame.image.load("assets/pieces.png")

#232 x 232 ?

w_king_rect = (0, 0, 232, 232)
w_queen_rect = (232, 0, 232, 232)

# generating squares

SQUARESIZE = 135
#SQUARESIZE = (SCREENWIDTH - (XBUFFER * 2)) / 8
DARK = (118, 150, 86)
LIGHT = (238, 238, 210)
FILES = ["A", "B", "C", "D", "E", "F", "G", "H"]
RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]

streaming_events = False
streaming_game = False

board_generated = False

Game = Game("")

Move = ["", ""]

def generate_squares(side):
  squares.clear() 

  for i in range(0, 8):
    for j in range(0, 8):
      x = int(i * SQUARESIZE) + XBUFFER
      y = int(j * SQUARESIZE)

      width = SQUARESIZE
      height = SQUARESIZE

      if i % 2 == 0:
        colour = LIGHT if (j % 2 == 0) else DARK
      else:
        colour = LIGHT if (j % 2 == 1) else DARK

      coords = FILES[i] + RANKS[(len(RANKS) - 1) - j] if (side == "WHITE") else FILES[(len(FILES) - 1) - i] + RANKS[j]
      
      sq = Square(coords, x, y, width, height, colour, myfont)
      squares[coords] = sq

def generate_e2e3e4():
  squares.clear()

  squares["E2"] = Square("E2", 300, 300, SQUARESIZE, SQUARESIZE, LIGHT, myfont)
  squares["E3"] = Square("E3", 300, 300 - SQUARESIZE, SQUARESIZE, SQUARESIZE, DARK, myfont)
  squares["E4"] = Square("E4", 300, 300 - (SQUARESIZE * 2), SQUARESIZE, SQUARESIZE, LIGHT, myfont)
  
# generate_squares("BLACK")

def generate_pieces():
  # squares["A1"] = Piece("Rook", 5, "WHITE", "")
  # squares["B1"] = Piece("Knight", 3, "WHITE", "")
  # squares["C1"] = Piece("Bishop", 3, "WHITE", "")
  squares["D1"].piece = Piece("Queen", 9, "WHITE", w_queen_rect, pieces_image)
  # squares["E1"] = Piece("King", 10, "WHITE", "")
  # squares["F1"] = Piece("Bishop", 3, "WHITE", "")
  # squares["G1"] = Piece("Knight", 3, "WHITE", "")
  # squares["H1"] = Piece("Rook", 5, "WHITE", "")

  # for i in FILES:
  #   squares[i + "2"] = Piece("Pawn", 1, "WHITE", "")

  # squares["A8"] = Piece("Rook", 5, "BLACK", "")
  # squares["B8"] = Piece("Knight", 3, "BLACK", "")
  # squares["C8"] = Piece("Bishop", 3, "BLACK", "")
  # squares["D8"] = Piece("Queen", 9, "BLACK", "")
  # squares["E8"] = Piece("King", 10, "BLACK", "")
  # squares["F8"] = Piece("Bishop", 3, "BLACK", "")
  # squares["G8"] = Piece("Knight", 3, "BLACK", "")
  # squares["H8"] = Piece("Rook", 5, "BLACK", "")

  # for j in FILES:
  #   squares[j + "7"] = Piece("Pawn", 1, "BLACK", "")

# event_stream = EventStream("", client, Game)
# event_stream.start()
# streaming_events = True

# client.challenges.create("SGBOY", False)

#generate_squares("WHITE")
generate_e2e3e4()

def getSquare(sqrs, event):
  for s in sqrs.values():
        if s.on_square(event.pos[0], event.pos[1]):
          return s.coordinates.lower()

while True: #Game Loop
  for event in pygame.event.get():
    if event.type in (QUIT, KEYDOWN):
      sys.exit()
    if event.type in (MOUSEBUTTONDOWN, FINGERDOWN):
      Move[0] = getSquare(squares, event)
    elif event.type in (MOUSEBUTTONUP, FINGERUP):
      Move[1] = getSquare(squares, event)
      print(Move)

    pygame.display.update()

    for s in squares.values():
      s.draw(SCREEN)
    # if not board_generated:
    #   print(Game.get_side())
    #   if Game.get_side() is not None:
    #     generate_squares(Game.get_side())
    #     generate_pieces()
    #     board_generated = True
      


  