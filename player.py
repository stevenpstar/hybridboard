
class Player:
  def __init__(self, ident, name, rating):
    self.id = ident
    self.name = name
    self.rating = rating

  def get_name(self):
    return self.name