import tdl

from components.fighter import Fighter

from input_handlers import handle_keys
from map_utils import GameMap, make_map, generate_monsters, generate_items
from entity import Entity, get_blocking_entity_at_location
from game_messages import MessageLog
from game_states import GameStates
from death_functions import kill_monster, kill_player
from render_functions import (
    RenderOrder, clear_all, render_all, render_health_bars, 
    render_messages)

def main():

    screen_width = 80
    screen_height = 50

    map_config = {
        'width': 80,
        'height': 43,
        'room_max_size': 15,
        'room_min_size': 6,
        'max_rooms': 30,
        'max_monsters_per_room': 3,
        'max_items_per_room': 2
    }

    panel_config = {
        'bar_width': 20,
        'height': 7,
    }
    panel_config['y'] = screen_height - panel_config['height']

    message_config = {
        'x': panel_config['bar_width'] + 2,
        'width': screen_width - panel_config['bar_width'] - 2,
        'height': panel_config['height'] - 1
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
        'darker_green': (0, 127, 0),
        'dark_red': (191, 0, 0),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'orange': (255, 127, 0),
        'light_red': (255, 144, 144),
        'darker_red': (127, 0, 0),
        'violet': (127, 0, 255),    
        'yellow': (255, 255, 0),
        'blue': (0, 0, 255),
        'green': (0, 255, 0)
    }

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    # Setup playscreen with two consoles:
    #  - A place to draw the playscreen with the map and entities.
    #  - A console with the player's health bar, and a message log.
    root_console = tdl.init(
       screen_width, screen_height,
       title='Rougelike Tutorial Game')
    map_console = tdl.Console(screen_width, screen_height)
    panel_console = tdl.Console(screen_width, panel_config['height'])
    message_log = MessageLog(message_config)

    # This is you.  Kill some Orcs.
    player = Entity(0, 0, '@', colors['white'], 'Player', 
                    fighter=Fighter(hp=20, defense=2, power=5),
                    blocks=True,
                    render_order=RenderOrder.ACTOR)
    entities = [player]
 
    # Generate the map and place player, monsters, and items.
    game_map = GameMap(map_config['width'], map_config['height'])
    rooms = make_map(game_map, map_config, player)
    monsters = generate_monsters(game_map, rooms, [player], map_config, colors)
    entities.extend(monsters)
    items = generate_items( game_map, rooms, entities, map_config, colors)
    entities.extend(items)
    
    # Initial values for game states
    fov_recompute = True
    game_state = GameStates.PLAYER_TURN

    #-------------------------------------------------------------------------
    # Main Game Loop.
    #-------------------------------------------------------------------------
    while not tdl.event.is_window_closed():

        # If needed, recompute the player's field of view.
        if fov_recompute:
            game_map.compute_fov(
                player.x, player.y,
                fov=fov_config["algorithm"],
                radius=fov_config["radius"],
                light_walls=fov_config["light_walls"])

        # Render and display the dungeon and its inhabitates.
        render_all(map_console, entities, game_map, fov_recompute, colors)
        root_console.blit(map_console, 0, 0, screen_width, screen_height, 0, 0)
        render_health_bars(panel_console, player, panel_config, colors)
        render_messages(panel_console, message_log)
        root_console.blit(panel_console, 0, panel_config['y'],
                          screen_width, screen_height, 0, 0)

        tdl.flush()
        clear_all(map_console, entities)

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
                # If you attempted to walk into a square occupied by an entity,
                # and that entity is not yourself.
                if blocker and blocker != player:
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
                message_log.add_message(message)
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
                message_log.add_message(death_message)
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
                message_log.add_message(message)
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
                message_log.add_message(death_message)
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

        #---------------------------------------------------------------------
        # If the player is dead, the game is over.
        #---------------------------------------------------------------------
        if game_state == GameStates.PLAYER_DEAD:
            continue


if __name__ == '__main__':
    main()
