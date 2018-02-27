import tdl

from components.fighter import Fighter

from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_utils import GameMap, make_map, generate_monsters
from entity import Entity, get_blocking_entity_at_location
from game_states import GameStates
from death_functions import kill_monster, kill_player

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
        'darker_green': (0, 127, 0),
        'dark_red': (191, 0, 0)
    }

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(
       screen_width, screen_height,
       title='Rougelike Tutorial Game')
    con = tdl.Console(screen_width, screen_height)

    player = Entity(0, 0, '@', colors['white'], 'Player', 
                    fighter=Fighter(hp=20, defense=2, power=5),
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

        #---------------------------------------------------------------------
        # Handle player move actions
        #---------------------------------------------------------------------
        # Get move action and check ccheck consequences.
        move = action.get('move')
        player_turn_results = []
        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x, destination_y = player.x + dx, player.y + dy
            if game_map.walkable[destination_x, destination_y]:
                blocker = get_blocking_entity_at_location(
                    entities, destination_x, destination_y)
                if blocker:
                    attack_results = player.fighter.attack(blocker)
                    player_turn_results.extend(attack_results)
                else:
                    player_turn_results.append({'move': (dx, dy)})
                game_state = GameStates.ENEMY_TURN
        # Process possible results of move action
        while player_turn_results != []:
            result = player_turn_results.pop()
            move = result.get('move')
            message = result.get('message')
            damage = result.get('damage')
            dead_entity = result.get('dead')
            death_message = result.get('death_message')
            # Handle movement.
            if move:
                player.move(*move)
                fov_recompute = True
            # Handle Messages
            if message:
                print(message)
            # Handle damage dealt.
            if damage:
                target, amount = damage
                damage_result = target.fighter.take_damage(amount)
                player_turn_results.extend(damage_result)
            # Handle death
            if dead_entity == player:
                player_turn_results.extend(kill_player(player, colors))
                game_state = GameStates.PLAYER_DEAD 
            elif dead_entity:
                player_turn_results.extend(
                    kill_monster(dead_entity, colors))
            # Handle a death message.  Death messages are special in that
            # they immediately break out of the game loop.
            if death_message:
                print(death_message)
                break

        #---------------------------------------------------------------------
        # Handle enemy actions
        #---------------------------------------------------------------------
        enemy_turn_results = []
        if game_state == GameStates.ENEMY_TURN:
            for entity in (x for x in entities if x.ai):
                enemy_turn_results.extend(entity.ai.take_turn(
                    player, game_map))
            game_state = GameStates.PLAYER_TURN
        # Process all result actions of enemy turns
        while enemy_turn_results != []:
            result = enemy_turn_results.pop()
            move_towards = result.get('move_towards')
            message = result.get('message')
            damage = result.get('damage')
            dead_entity = result.get('dead')
            death_message = result.get('death_message')
            # Handle a move towards action.  Move towards a target.
            if move_towards:
               monster, target_x, target_y = move_towards
               monster.move_towards(target_x, target_y, game_map, entities)
            # Handle a simple message.
            if message:
                print(message)
            # Handle damage dealt.
            if damage:
                target, amount = damage
                damage_result = target.fighter.take_damage(amount)
                enemy_turn_results.extend(damage_result)
            # Handle death.
            if dead_entity == player:
                enemy_turn_results.extend(kill_player(player, colors))
                game_state = GameStates.PLAYER_DEAD 
            elif dead_entity:
                enemy_turn_results.extend(
                    kill_monster(dead_entity, colors))
            # Handle a death message.  Death messages are special in that
            # they immediately break out of the game loop.
            if death_message:
                print(death_message)
                break

        #---------------------------------------------------------------------
        # If the player is dead, the game is over.
        #---------------------------------------------------------------------
        if game_state == GameStates.PLAYER_DEAD:
            break

        #---------------------------------------------------------------------
        # Handle meta actions
        #---------------------------------------------------------------------
        exit = action.get('exit')
        if exit:
            return True
        fullscreen = action.get('fullscreen')
        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()
