import pygame
from pygame.locals import *
from piece import Piece

class Square:
  def __init__(self, coords, x, y, width, height, colour, font):
    self.coordinates = coords
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.colour = colour
    self.font = font
    self.piece = None

  def get_coordinates(self):
    return self.coordinates

  def draw(self, SCREEN):
    pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.width, self.height))
    self.font.render_to(SCREEN, (self.x + self.width - 46, self.y + self.height - 32), self.coordinates, 
    (self.colour[0] - 10, self.colour[1] - 10, self.colour[2] - 10))
    if type(self.piece) == Piece:
        self.piece.draw(self.x, self.y, SCREEN)
  
  def on_square(self, x, y):
    if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
      return True
    else:
      return False
  
  def get_piece(self):
    return self.piece

  def set_piece(self, piece):
    self.piece = piece