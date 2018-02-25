import tdl
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_utils import GameMap, make_map
from entity import Entity

def main():

    screen_width = 80
    screen_height = 50

    map_config = {
        'width': 80,
        'height': 45,
        'room_max_size': 15,
        'room_min_size': 6,
        'max_rooms': 30
    }

    fov_config = {
        "algorithm": 'BASIC',
        "light_walls": True,
        "radius": 10
    }

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        'desaturated_green': (63, 127, 63),
        'darker_green': (0, 127, 0)
    }

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(
       screen_width, screen_height,
       title='Rougelike Tutorial Game')
    con = tdl.Console(screen_width, screen_height)

    player = Entity(int(screen_width / 2), int(screen_height / 2),
                    '@', (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2),
                 '@', (255, 255, 0))
    entities = [player, npc]

    game_map = GameMap(map_config['width'], map_config['height'])
    make_map(game_map, map_config, player)
    
    fov_recompute = True

    while not tdl.event.is_window_closed():

        if fov_recompute:
            game_map.compute_fov(
                player.x, player.y,
                fov=fov_config["algorithm"],
                radius=fov_config["radius"],
                light_walls=fov_config["light_walls"])

        render_all(con, entities, game_map, fov_recompute, colors)
        root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)
        tdl.flush()
        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        if not user_input:
            continue

        action = handle_keys(user_input)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)
                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()
                             
