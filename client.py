import berserk
import threading
from game import Game
from player import Player
from queue import Queue


class GameStream(threading.Thread):
  def __init__(self, game_id, client, game):
    super().__init__()
    self.game_id = game_id
    self.client = client
    self.stream = self.client.board.stream_game_state(game_id)
    self.moves = []
    self.me = None
    self.opposition = None
    self.game = game

  def run(self):
    for event in self.client.board.stream_game_state(self.game_id):
      print(event)
      # get player sides
      if 'white' in event:
        if event['white']['id'] == 'stevenpstar':
          print('Setting to White')
          self.game.set_side("WHITE")
        else:
          print('Setting to Black')
          self.game.set_side("BLACK")



class EventStream(threading.Thread):
  def __init__(self, token, client, game):
    super().__init__()
    self.token = token
    self.client = client
    self.stream = self.client.board.stream_incoming_events()
    self.game = game
  
  def run(self):
    for inc_event in self.stream:
      print(inc_event)
      if inc_event['type'] == 'challengeDeclined':
        return
      elif inc_event['type'] == 'gameStart':
        print(inc_event)
        game_id = inc_event['game']
        print("ID")
        print(game_id)
        self.game.game_id = game_id['id']
        game = GameStream(game_id['id'], self.client, self.game)
        game.start()




# for event in client.board.stream_game_state(gameId):
#   print(event)
#   print(moves)
#   if 'moves' in event:
#     moves = event['moves']

#   if len(moves) % 2 == 0:
#     value = input("Move: ")
#     try:
#       client.board.make_move(gameId, value)
#     except:
#       print("Uh oh try again?")

# for event in client.board.stream_incoming_events():
#   print(event['type'])

#   if event['type'] == 'gameStart':
#     print(event)
#     if gameId == "none":
#       gameId = "nYnr74vr"
#       print("Setting ID and starting Game?")
#       game = Game(gameId)
#       game.start()

