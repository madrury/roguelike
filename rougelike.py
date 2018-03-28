import tdl

from components.fighter import Fighter
from components.inventory import Inventory

from input_handlers import handle_keys
from game_messages import Message
from map_utils import GameMap, make_map, generate_monsters, generate_items
from entity import Entity, get_blocking_entity_at_location
from game_messages import MessageLog
from game_states import GameStates
from menus import invetory_menu
from death_functions import kill_monster, kill_player
from render_functions import (
    RenderOrder, clear_all, render_all, render_health_bars, 
    render_messages)


def main():

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    MAP_CONFIG = {
        'width': 80,
        'height': 43,
        'room_max_size': 15,
        'room_min_size': 6,
        'max_rooms': 30,
        'max_monsters_per_room': 3,
        'max_items_per_room': 2
    }

    PANEL_CONFIG = {
        'bar_width': 20,
        'height': 7,
    }
    PANEL_CONFIG['y'] = SCREEN_HEIGHT - PANEL_CONFIG['height']

    message_config = {
        'x': PANEL_CONFIG['bar_width'] + 2,
        'width': SCREEN_WIDTH - PANEL_CONFIG['bar_width'] - 2,
        'height': PANEL_CONFIG['height'] - 1
    }

    FOV_CONFIG = {
        "algorithm": 'BASIC',
        "light_walls": True,
        "radius": 10
    }

    COLORS = {
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
       SCREEN_WIDTH, SCREEN_HEIGHT,
       title='Rougelike Tutorial Game')
    map_console = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    panel_console = tdl.Console(SCREEN_WIDTH, PANEL_CONFIG['height'])
    message_log = MessageLog(message_config)

    # This is you.  Kill some Orcs.
    player = Entity(0, 0, '@', COLORS['white'], 'Player', 
                    blocks=True,
                    render_order=RenderOrder.ACTOR,
                    fighter=Fighter(hp=20, defense=2, power=5),
                    inventory=Inventory(26))
    entities = [player]
 
    # Generate the map and place player, monsters, and items.
    game_map = GameMap(MAP_CONFIG['width'], MAP_CONFIG['height'])
    rooms = make_map(game_map, MAP_CONFIG, player)
    monsters = generate_monsters(game_map, rooms, [player], MAP_CONFIG, COLORS)
    entities.extend(monsters)
    items = generate_items( game_map, rooms, entities, MAP_CONFIG, COLORS)
    entities.extend(items)
    
    # Initial values for game states
    fov_recompute = True
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state

    #-------------------------------------------------------------------------
    # Main Game Loop.
    #-------------------------------------------------------------------------
    while not tdl.event.is_window_closed():

        # If needed, recompute the player's field of view.
        if fov_recompute:
            game_map.compute_fov(
                player.x, player.y,
                fov=FOV_CONFIG["algorithm"],
                radius=FOV_CONFIG["radius"],
                light_walls=FOV_CONFIG["light_walls"])

        # Render and display the dungeon and its inhabitates.
        render_all(map_console, entities, game_map, fov_recompute, COLORS)
        root_console.blit(map_console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        render_health_bars(panel_console, player, PANEL_CONFIG, COLORS)
        render_messages(panel_console, message_log)
        root_console.blit(panel_console, 0, PANEL_CONFIG['y'],
                          SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

        # Render any menus.
        if game_state in (GameStates.SHOW_INVETORY, GameStates.DROP_INVENTORY):
            if game_state == GameStates.SHOW_INVETORY:
                invetory_message = "Press the letter next to the item to use it.\n"
            elif game_state == GameStates.DROP_INVENTORY:
                invetory_message = "Press the letter next to the item to drop it.\n"
            menu_console, menu_x, menu_y = invetory_menu(
                invetory_message, player.inventory, 50,
                SCREEN_WIDTH, SCREEN_HEIGHT)
            root_console.blit(menu_console, menu_x, menu_y,
                              SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

        tdl.flush()
        clear_all(map_console, entities)

        # Unless the player moves, we do not need to recompute the fov.
        fov_recompute = False 

        #---------------------------------------------------------------------
        # Get key input from the player.
        #---------------------------------------------------------------------
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        if not user_input:
            continue
        action = handle_keys(user_input, game_state)

        #----------------------------------------------------------------------
        # Handle player actions.
        #......................................................................
        # Here we process the consequences of input from the player that
        # affect the game state.  These consequences are added to a queue for
        # later processing.  This allows consequences to have further 
        # consequences, which are then also added to the queue.  The messages
        # on the queue are constantly popped and dealt with until the queue is
        # empty, after which we pass the turn.
        #----------------------------------------------------------------------
        move = action.get('move')
        pickup = action.get('pickup')
        drop = action.get('drop')
        inventory_index = action.get('inventory_index')
        player_turn_results = []

        #----------------------------------------------------------------------
        # Player Move Action
        #......................................................................
        # The player has entered a move action.  Chack if the space in that
        # direction is movable, and if so put a move result on the queue.  If
        # if not, attack the blocking entity by putting an attack action on the
        # queue.
        #----------------------------------------------------------------------
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

        #----------------------------------------------------------------------
        # Player Pickup
        #......................................................................
        # The player has attempted to pickup an item.  If there is an item in
        # the players space, put a pickup action on the queue.
        #----------------------------------------------------------------------
        elif pickup and game_state == GameStates.PLAYER_TURN:
            for entity in entities:
                if (entity.item
                    and entity.x == player.x and entity.y == player.y):
                    pickup_results = player.inventory.pickup(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                player_turn_results.append({
                    'message': Message("There is nothing to pick up!")})
            game_state = GameStates.ENEMY_TURN

        #----------------------------------------------------------------------
        # Player Inventory use / drop
        #......................................................................
        # The player has attempted to use or drop an item from the inventory.
        # Check which state we are in (using or dropping) and put an
        # instruction on the queue.
        #----------------------------------------------------------------------
        elif (game_state in (GameStates.SHOW_INVETORY, GameStates.DROP_INVENTORY)
            and inventory_index is not None
            and inventory_index < len(player.inventory.items)
            and previous_game_state != GameStates.PLAYER_DEAD):
            entity = player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVETORY:
                if entity.item.use_on_player:
                    player_turn_results.extend(entity.item.use(player, COLORS))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop(entity))
            game_state, previous_game_state = previous_game_state, game_state

        #----------------------------------------------------------------------
        # Process the results queue 
        #......................................................................
        # We are done processing player inputs, and may have some results on
        # the player turn queue.  Process the queue by popping off the top
        # result from the queue.  There are many different possible results,
        # so handle each with a dedicated handler.
        #
        # Note: Handling a result may result in other results being added to
        # the queue, so we continually process the results queue until it is
        # empty.
        #----------------------------------------------------------------------
        while player_turn_results != []:
            result = player_turn_results.pop()
            move = result.get('move')
            message = result.get('message')
            item_added = result.get('item_added')
            damage = result.get('damage')
            item_consumed = result.get('item_consumed')
            item_dropped = result.get('item_dropped')
            heal = result.get('heal')
            dead_entity = result.get('dead')
            death_message = result.get('death_message')
            # Handle movement.
            if move:
                player.move(*move)
                fov_recompute = True
            # Handle Messages
            if message:
                message_log.add_message(message)
            if item_added:
                player.inventory.add(item_added)
                entities.remove(item_added)
            # Handle damage dealt.
            if damage:
                target, amount = damage
                damage_result = target.fighter.take_damage(amount)
                player_turn_results.extend(damage_result)
            # Remove consumed items from inventory
            if item_consumed:
                consumed, item = item_consumed
                if consumed:
                    player.inventory.remove(item)
                    game_state, previous_game_state = (
                        GameStates.ENEMY_TURN, game_state)
            # Remove dropped items from inventory and place on the map
            if item_dropped:
                player.inventory.remove(item_dropped)
                item_dropped.x, item_dropped.y = player.x, player.y
                entities.append(item_dropped)
                game_state, previous_game_state = (
                    GameStates.ENEMY_TURN, game_state)
            # Heal an entity
            if heal:
                target, amount = heal
                target.fighter.hp += min(
                    amount, target.fighter.max_hp - target.fighter.hp)
            # Handle death
            if dead_entity == player:
                player_turn_results.extend(kill_player(player, COLORS))
                game_state = GameStates.PLAYER_DEAD 
            elif dead_entity:
                player_turn_results.extend(
                    kill_monster(dead_entity, COLORS))
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
                enemy_turn_results.extend(kill_player(player, COLORS))
                game_state = GameStates.PLAYER_DEAD 
            elif dead_entity:
                enemy_turn_results.extend(
                    kill_monster(dead_entity, COLORS))
            # Handle a death message.  Death messages are special in that
            # they immediately break out of the game loop.
            if death_message:
                message_log.add_message(death_message)
                break

        #---------------------------------------------------------------------
        # Handle meta actions
        #---------------------------------------------------------------------
        show_invetory = action.get('show_invetory')
        if game_state == GameStates.PLAYER_TURN and show_invetory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVETORY

        drop = action.get('drop_inventory')
        if game_state == GameStates.PLAYER_TURN and drop:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        exit = action.get('exit')
        if exit:
            if game_state in (
                GameStates.SHOW_INVETORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
                # Hard exit the game.
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
