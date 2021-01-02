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
from touchtimer import TouchTimer

session = berserk.TokenSession('V4lt6pmQmgrbzgIB')
client = berserk.Client(session)

is_polite = True

gameId = "nYnr74vr"

moves = []

pygame.init()

SCREENWIDTH = 1920
SCREENHEIGHT = 1080
XBUFFER = (SCREENWIDTH - SCREENHEIGHT) / 2

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
SCREEN.fill((0, 0, 0))

squares = {}
pieces = {}
Timer = TouchTimer(1620, 0, 300, 1080)

Timer2 = TouchTimer(0, 0, 300, 1080)
myfont = pygame.freetype.SysFont('Verdana', 30)

filename = 'assets/pieces.png'
#pieces_image = pygame.image.load("assets/pieces.png")


#232 x 232 ?

w_king_rect = (0, 0, 232, 232)
w_queen_rect = (232, 0, 232, 232)

# generating squares

#SQUARESIZE = 135
SQUARESIZE = (SCREENWIDTH - (XBUFFER * 2)) / 8
DARK = (118, 150, 86)
LIGHT = (238, 238, 210)
FILES = ["A", "B", "C", "D", "E", "F", "G", "H"]
RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]

b_pawn = pygame.image.load("assets/blackpawn.png")
b_pawn = pygame.transform.scale(b_pawn, (int(SQUARESIZE), int(SQUARESIZE)))

b_rook = pygame.image.load("assets/blackrook.png")
b_rook = pygame.transform.scale(b_rook, (int(SQUARESIZE), int(SQUARESIZE)))

b_king = pygame.image.load("assets/blackking.png")
b_king = pygame.transform.scale(b_king, (int(SQUARESIZE), int(SQUARESIZE)))

b_bishop = pygame.image.load("assets/blackbishop.png")
b_bishop = pygame.transform.scale(b_bishop, (int(SQUARESIZE), int(SQUARESIZE)))

b_queen = pygame.image.load("assets/blackqueen.png")
b_queen = pygame.transform.scale(b_queen, (int(SQUARESIZE), int(SQUARESIZE)))

b_knight = pygame.image.load("assets/blackknight.png")
b_knight = pygame.transform.scale(b_knight, (int(SQUARESIZE), int(SQUARESIZE)))

streaming_events = False
streaming_game = False

board_generated = False

Game = Game("")

Move = ["", ""]
FirstTouchDown = ""

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

  xOff = 200

  squares["D2"] = Square("D2", xOff + SQUARESIZE, 300, SQUARESIZE, SQUARESIZE, DARK, None)
  squares["D3"] = Square("D3", xOff + SQUARESIZE, 300 - SQUARESIZE, SQUARESIZE, SQUARESIZE, LIGHT, None)
  squares["D4"] = Square("D4", xOff + SQUARESIZE, 300 - (SQUARESIZE * 2), SQUARESIZE, SQUARESIZE, DARK, None)

  squares["E2"] = Square("E2", xOff + (SQUARESIZE * 2), 300, SQUARESIZE, SQUARESIZE, LIGHT, None)
  squares["E3"] = Square("E3", xOff + (SQUARESIZE * 2), 300 - SQUARESIZE, SQUARESIZE, SQUARESIZE, DARK, None)
  squares["E4"] = Square("E4", xOff + (SQUARESIZE * 2), 300 - (SQUARESIZE * 2), SQUARESIZE, SQUARESIZE, LIGHT, None)

  squares["F2"] = Square("F2", xOff + (SQUARESIZE * 3), 300, SQUARESIZE, SQUARESIZE, DARK, None)
  squares["F3"] = Square("F3", xOff + (SQUARESIZE * 3), 300 - SQUARESIZE, SQUARESIZE, SQUARESIZE, LIGHT, None)
  squares["F4"] = Square("F4", xOff + (SQUARESIZE * 3), 300 - (SQUARESIZE * 2), SQUARESIZE, SQUARESIZE, DARK, None)
  
def generate_pieces():
  # squares["A1"] = Piece("Rook", 5, "WHITE", "")
  # squares["B1"] = Piece("Knight", 3, "WHITE", "")
  # squares["C1"] = Piece("Bishop", 3, "WHITE", "")
  # squares["D1"].piece = Piece("Queen", 9, "WHITE", w_queen_rect, pieces_image)
  # squares["E1"] = Piece("King", 10, "WHITE", "")
  # squares["F1"] = Piece("Bishop", 3, "WHITE", "")
  # squares["G1"] = Piece("Knight", 3, "WHITE", "")
  # squares["H1"] = Piece("Rook", 5, "WHITE", "")

  # for i in FILES:
  #   squares[i + "2"] = Piece("Pawn", 1, "WHITE", "")

  squares["A8"].piece = Piece("Rook", 5, "BLACK", b_rook)
  squares["B8"].piece = Piece("Knight", 3, "BLACK", b_knight)
  squares["C8"].piece = Piece("Bishop", 3, "BLACK", b_bishop)
  squares["D8"].piece = Piece("Queen", 9, "BLACK", b_queen)
  squares["E8"].piece = Piece("King", 10, "BLACK", b_king)
  squares["F8"].piece = Piece("Bishop", 3, "BLACK", b_bishop)
  squares["G8"].piece = Piece("Knight", 3, "BLACK", b_knight)
  squares["H8"].piece = Piece("Rook", 5, "BLACK", b_rook)

  for j in FILES:
    squares[j + "7"].piece = Piece("Pawn", 1, "BLACK", b_pawn)

event_stream = EventStream("", client, Game)
event_stream.start()
streaming_events = True

#client.challenges.create("SGBOY", False, None, None, None, "white", None, None)
client.challenges.create_ai(8, None, None,None,"white")

#we need to track the last touch up coordinates

def render_moves():
  #print("Should constantly be called")
  if Game.moves == Game.saved_moves:
    return 
  mvs = Game.moves.split()
  mv = mvs[-1]
  frm = mv[0:2]
  to = mv[2:]

  squares[to.upper()].piece = None
  squares[to.upper()].piece = squares[frm.upper()].piece
  squares[frm.upper()].piece = None

  Game.saved_moves = Game.moves

lastTouchUp = None

generate_squares("WHITE")
generate_pieces()
#generate_e2e3e4()

def validate_move(Move):
  if Move[0] == "":
    print("First Empty")
    return False
  if Move[1] == "":
    print("Second empty")
    return False
  if Move[0] == Move[1]:
    print("Same place")
    return False
  return True

def getSquare(sqrs, event):
#  mx, my = pygame.mouse.get_pos()
  mx = event.x * 1920
  my = event.y * 1080
  print(mx, my)
  for s in sqrs.values():
        if s.on_square(mx, my):
          print("On square: " + s.coordinates.lower())
          return s.coordinates.lower()
  return None

def try_move(game_id, move):
  #print(move)
  if validate_move(move):
     try:
       mv = move[0] + move[1]
       client.board.make_move(Game.game_id, mv)
     except:
       print("Illegal move bb")
  else:
    if move[0] != "" and move[1] != "":
      Move = ["", ""]

def my_turn(colour, mvs):
  # for now my colour is always white
  mv = mvs.split()
  if len(mv) % 2 == 0:
    return True
  return False

def square_not_occupied(squares, event):
  # mx = event.x * 1920
  # my = event.y * 1080
  # for s in squares.values():
  #       if s.on_square(mx, my):
  #         return s.piece == None or s.piece.colour != "white"
  return True


while True: #Game Loop
  render_moves()
  for event in pygame.event.get():
    if event.type == (QUIT):
      sys.exit()
    if my_turn("white", Game.moves):
      print(Game.moves)
      if event.type == FINGERUP:
        if square_not_occupied(squares, event):
          lastTouchUp = getSquare(squares, event)
        else:
          print("Square occupied")

      elif event.type == FINGERDOWN:
          mx, my = pygame.mouse.get_pos()
          if Timer.on_square(mx, my):
              Move[1] = lastTouchUp
              try_move(Game.game_id, Move)
          elif Timer2.on_square(mx, my):
              Move = ["", ""]
              FirstTouchDown = ""
          else:
              if Move[0] == "":
                  Move[0] = getSquare(squares, event)
                  FirstTouchDown = Move[0]
                  print(Move[0])
                  if Move[0] == None:
                      Move[0] = ""
                      FirstTouchDown = ""
      
    
    Timer.draw(SCREEN)
    Timer2.draw(SCREEN)

  for s in squares.values():
    s.draw(SCREEN)
  pygame.display.update()
    #if not board_generated:
      #if Game.get_side() is not None:
       # generate_squares(Game.get_side())
       # generate_pieces()
       # board_generated = True