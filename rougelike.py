import tdl

from components.fighter import Fighter

from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_utils import GameMap, make_map, generate_monsters
from entity import Entity, get_blocking_entity_at_location
from game_states import GameStates

def main():

    screen_width = 80
    screen_height = 50

    map_config = {
        'width': 80,
        'height': 45,
        'room_max_size': 15,
        'room_min_size': 6,
        'max_rooms': 30,
        'max_monsters_per_room': 3
    }

    fov_config = {
        "algorithm": 'BASIC',
        "light_walls": True,
        "radius": 10
    }

    colors = {
        'white': (255, 255, 255),
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

    player = Entity(0, 0, '@', colors['white'], 'Player', 
                    fighter=Fighter(hp=30, defense=2, power=5),
                    blocks=True)
    entities = [player]

    game_map = GameMap(map_config['width'], map_config['height'])
    rooms = make_map(
        game_map, map_config, player)
    monsters = generate_monsters(
        game_map, rooms, player, map_config, colors)
    entities.extend(monsters)
    
    # Initial values for game states
    fov_recompute = True
    game_state = GameStates.PLAYER_TURN

    while not tdl.event.is_window_closed():

        # If needed, recompute the player's field of view.
        if fov_recompute:
            game_map.compute_fov(
                player.x, player.y,
                fov=fov_config["algorithm"],
                radius=fov_config["radius"],
                light_walls=fov_config["light_walls"])

        # Render and display the dungeon and its inhabitates.
        render_all(con, entities, game_map, fov_recompute, colors)
        root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)
        tdl.flush()
        clear_all(con, entities)

        # Unless the player moves, we do not need to recompute the fov.
        fov_recompute = False 

        # Get input from the player.
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        if not user_input:
            continue
        action = handle_keys(user_input)

        # Handle player actions
        move = action.get('move')
        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x, destination_y = player.x + dx, player.y + dy
            if game_map.walkable[destination_x, destination_y]:
                blocker = get_blocking_entity_at_location(
                    entities, destination_x, destination_y)
                if blocker:
                    player.fighter.attack(blocker)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN

        exit = action.get('exit')
        if exit:
            return True

        if game_state == GameStates.ENEMY_TURN:
            for entity in (x for x in entities if x.ai):
                entity.ai.take_turn(player, game_map, entities)
            game_state = GameStates.PLAYER_TURN

        fullscreen = action.get('fullscreen')
        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()
