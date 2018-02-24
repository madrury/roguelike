from random import randint

class Rectangle:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


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

def make_map(game_map, max_rooms, 
             room_min_size, room_max_size, 
             map_width, map_height, player):

    rooms = []
    for r in range(max_rooms):
        width = randint(room_min_size, room_max_size)
        height = randint(room_min_size, room_max_size)
        x = randint(0, map_width - width - 1)
        y = randint(0, map_height - height - 1)

        new_room = Rectangle(x, y, width, height)
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            create_room(game_map, new_room)

        cx, cy = new_room.center
        num_rooms = len(rooms)
        if num_rooms == 0:
            player.x, player.y = cx, cy
        else:
            prev_x, prev_y = rooms[num_rooms - 1].center
            if randint(0, 1) == 1:
                create_h_tunnel(game_map, prev_x, cx, prev_y)
                create_v_tunnel(game_map, prev_y, cy, cx)
            else:
                create_v_tunnel(game_map, prev_y, cy, prev_x)
                create_h_tunnel(game_map, prev_x, cx, cy)

        rooms.append(new_room)
            
            

