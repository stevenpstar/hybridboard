class Game:
  def __init__(self, game_id):
    self.game_id = game_id
    self.side = None
    self.moves = ""
    self.saved_moves = ""

  def set_side(self, side):
    self.side = side

  def get_side(self):
    return self.side