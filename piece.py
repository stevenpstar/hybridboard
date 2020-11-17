import pygame

class Piece:
  def __init__(self, pt, value, colour, rect, image):
    self.piece = pt #[piece type]
    self.value = value
    self.colour = colour
    self.image = image
    self.rect = rect
    self.square = None

  def set_square(self, square):
    self.square = square

  def draw(self, x, y, SCREEN):
    SCREEN.blit(self.image, (x, y), self.rect)