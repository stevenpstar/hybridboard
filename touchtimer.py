import pygame

class TouchTimer:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = (0, 0, 255)

    def on_square(self, x, y):
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            return True
        else:
            return False


    def draw(self, SCREEN): 
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.width, self.height))