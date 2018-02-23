
class Rectangle:

  def __init__(self, x, y, w, h):
      self.x1 = x
      self.y1 = y
      self.x2 = x + w
      self.y2 = y + h

def create_room(game_map, room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            make_transparent_and_walkable(game_map, x, y)

def create_h_tunnel(game_map, x1, x2, y):
    x1, x2 = min(x1, x2), max(x1, x2)
    for x in range(x1, x2 + 1):
        make_transparent_and_walkable(game_map, x, y)

def create_v_tunnel(game_map, y1, y2, x):
    y1, y2 = min(y1, y2), max(y1, y2)
    for y in range(y1, y2 + 1):
        make_transparent_and_walkable(game_map, x, y)

def make_transparent_and_walkable(game_map, x, y):
    game_map.walkable[x, y] = True
    game_map.transparent[x, y] = True

# Test code
def make_map(game_map):
    room1 = Rectangle(20, 15, 10, 15)
    room2 = Rectangle(35, 15, 10, 15)
    create_room(game_map, room1)
    create_room(game_map, room2)
    create_h_tunnel(game_map, 30, 35, 20)

