from collections import deque
from time import sleep

import tdl

from animations.animations import construct_animation

from components.status_manager import (
    PlayerConfusedManager, EnemyConfusedManager,
    EnemyFrozenManager, SpeedManager)

from etc.colors import COLORS
from etc.config import (
    N_FLOORS, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_PANEL_CONFIG,
    BOTTOM_PANEL_CONFIG, MAP_PANEL_CONFIG, MESSAGE_CONFIG, FOV_CONFIG,
    ANIMATION_INTERVAL, SHIMMER_INTERVAL, INITIAL_PLAYER_POSITION)
from etc.enum import (
    ResultTypes, FloorResultTypes, InputTypes, EntityTypes, GameStates,
    INVENTORY_STATES, INPUT_STATES, CANCEL_STATES)

from generation.floor_schedule import FLOOR_SCHEDULES

from utils.debug import highlight_array, highlight_stairs, highlight_rooms
from utils.utils import (
    flatten_list_of_dictionaries,
    unpack_single_key_dict,
    get_key_from_single_key_dict,
    get_all_entities_with_component_in_position)

from cursor import Cursor
from death_functions import kill_monster, kill_player, make_corpse
from game_loop_functions import (
    create_map, create_player, set_all_ai_targets, construct_inventory_data,
    get_user_input, process_selected_item, player_move_or_attack,
    pickup_entity, encroach_on_all, process_damage, process_harm, apply_status,
    entity_equip_armor, entity_equip_weapon, entity_remove_armor,
    entity_remove_weapon)
from menus import invetory_menu
from messages import MessageLog


def main():
    """Entry point for starting the game, and managing the high level game
    state.

    This function is responsible for:

      - Setting up the main game resources.  Windows and consoles.
      - Sets up the main game variables, the player, and an array for tracking
        the floors in the dungeon.
      - Starts the main loop, which calls into the function to play a floor.
      - Manages the high level game state: what is the turn number, what floor
        is the player currently on?
    """
    # TODO: Remove N_FLOORS from config.

    tdl.set_font('fonts/consolas10x10.png', greyscale=True, altLayout=True)
    # Setup playscreen with two consoles:
    #  - A place to draw the playscreen with the map and entities.
    #  - A console with the player's health bar, and a message log.
    root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT,
                            title='Roguelike Tutorial Game')
    map_console = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    top_panel_console = tdl.Console(
        SCREEN_WIDTH, TOP_PANEL_CONFIG['height'])
    bottom_panel_console = tdl.Console(
        SCREEN_WIDTH, BOTTOM_PANEL_CONFIG['height'])
    consoles = [
        root_console, map_console, bottom_panel_console, top_panel_console]
    # TODO: 3 is number of floors, break this into a config element.
    game_maps = [None] * N_FLOORS
    # Create the map for the first floor of the dungeon and place the player.
    game_maps[0] = create_map(map_console, floor_schedule=FLOOR_SCHEDULES[0])
    player = create_player(game_maps[0])
    player.x, player.y = INITIAL_PLAYER_POSITION
    # All monster entities initially target the player:
    set_all_ai_targets(game_maps[0], player)
    # Track the current turn of the game.  Used for events that happen on a
    # fixed schedule.
    game_turn = 0
    # The current floor of the dungeon.  Starts at floor zero, hopefully the
    # player descendes far into the dungeon!
    current_floor = 0
    while True:
        # If we do not clear the consoles before begining to play the floor, a
        # ghost image of the prior floor will remain.
        for console in consoles:
            console.clear()
        # If we have not yet generated a map for this floor of the dungeon, do
        # so now.
        current_map = game_maps[current_floor]
        if current_map == None:
            current_map = create_map(
                map_console,
                floor_schedule=FLOOR_SCHEDULES[current_floor])
            set_all_ai_targets(current_map, player)
            game_maps[current_floor] = current_map
        # If we are not on the first turn of the game, place the player at the
        # appropriate staircase.
        if game_turn != 0:
            if floor_result == FloorResultTypes.DECREMENT_FLOOR:
                player.x, player.y = current_map.upward_stairs_position
            if floor_result == FloorResultTypes.INCREMENT_FLOOR:
                player.x, player.y = current_map.downward_stairs_position
        # Add the player to the entities on the current floor.
        current_map.entities.append(player)
        # Ok, let's play!
        floor_result, game_turn = play_floor(
            current_map, player, consoles,
            game_turn=game_turn,
            current_floor=current_floor)
        # This position is reached after the player is done with a floor of the
        # dungeon, there are three options:
        #  - The player is descending to the next floor.
        #  - The player is ascending to the previous floor.
        #  - The player ended the game.
        if floor_result == FloorResultTypes.END_GAME:
            return True
        current_floor = (current_floor + floor_result.value) % 3


def play_floor(game_map, player, consoles, *, game_turn, current_floor):
    """Play a floor of the dungeon.

    This function contains the main game loop.  This loop controls the flow for
    a single turn of the game.

    A generic turn progresses through the following general phases:

      - Get player input.
      - Compute and then execute consequences of that input.
      - Complete status and environment checks post player turn.
      - All enemies and environmental hazards take turns.

    In addition, during special game states, the main game loop is also
    responsible for:

      - Playing animations (each tick of the game loop progresses the animation
        one frame).
      - Moving a cursor during cursor input events (i.e. targeting a staff or
        thrown potion).
    """
    #-------------------------------------------------------------------------
    # Game State Varaibles
    #-------------------------------------------------------------------------
    root_console, _, bottom_panel_console, top_panel_console = consoles
    # Initial values for game states
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    # After an animation finishes, we need to continue processing the stack of
    # player turn results (animations are popped off first, so there will still
    # be results from the previous turn on the stack).  This flag will skip the
    # gathering of user input which ususally occurs before processing the
    # player turn stack.
    skip_player_input = False
    # This will be populated when we are playing an animation.  Call
    # .next_frame on this object to draw the next frame of the animation. This
    # method returns False until the animation is finished, after the last
    # frame is player, will return True.
    animation_player = None
    # A queue for storing enemy targets that have taken damage.  Used to render
    # enemy health bars in the UI.
    harmed_queue = deque(maxlen=3)
    # A cursor object for allowing the user to select a space on the map, will
    # be populated when the game state is in cursor select mode.
    cursor = None
    # Stacks for holding the results of player and enemy turns.
    player_turn_results = []
    enemy_turn_results = []
    # Log of game messages.
    message_log = MessageLog(MESSAGE_CONFIG)
    # A counter for how many times we have incremented the game loop on this
    # floor.  Used to trigger updates that happen regularly with regards to
    # game loop.  For example, graphical shimmering of water and ice.
    game_loop = -1

    #-------------------------------------------------------------------------
    # Main Game Loop.
    #-------------------------------------------------------------------------
    while not tdl.event.is_window_closed():

        game_loop += 1

        #---------------------------------------------------------------------
        # Game loop variables
        #---------------------------------------------------------------------
        user_input = None

        #---------------------------------------------------------------------
        # Recompute the player's field of view.
        #---------------------------------------------------------------------
        game_map.compute_fov(
            player.x, player.y,
            fov=FOV_CONFIG["algorithm"],
            radius=FOV_CONFIG["radius"],
            light_walls=FOV_CONFIG["light_walls"])

        #---------------------------------------------------------------------
        # Shimmer the colors of entities that shimmer.
        #---------------------------------------------------------------------
        if game_loop % SHIMMER_INTERVAL == 0:
            for entity in game_map.entities:
                if entity.shimmer:
                    entity.shimmer.shimmer()

        #---------------------------------------------------------------
        # Clear the illumination array, which is recomputed from scratch
        # each time terrain takes their turns.
        #---------------------------------------------------------------
        if game_state == GameStates.PLAYER_TURN:
            game_map.illuminated[:, :] = 0
            for entity in (e for e in game_map.entities if e.illuminatable):
                entity.illuminatable.illuminate(game_map)

        #---------------------------------------------------------------------
        # Render and display the dungeon and its inhabitates.
        #---------------------------------------------------------------------
        game_map.update_and_draw_all()

        #---------------------------------------------------------------------
        # Render the UI
        #---------------------------------------------------------------------
        # Top panel.
        top_panel_console.clear(fg=COLORS['white'], bg=COLORS['black'])
        top_panel_console.draw_str(0, 0,
            f" Current Floor: {current_floor}  Turn Number: {game_turn} "
            f" Position: {player.x}, {player.y}",
            fg=(255, 255, 255))
        player.harmable.render_status_bar(top_panel_console, 1, 2)
        player.swimmable.render_status_bar(
            top_panel_console, TOP_PANEL_CONFIG['bar_width'] + 2, 2)
        if player.status_manager:
            player.status_manager.render_status_bar(
                top_panel_console, 2*TOP_PANEL_CONFIG['bar_width'] + 4, 2)
        # Bottom panel.
        bottom_panel_console.clear(fg=COLORS['white'], bg=COLORS['black'])
        for idx, entity in enumerate(e for e in harmed_queue if e != player):
            entity.harmable.render_status_bar(
                bottom_panel_console, 1, 2*idx + 1)
        message_log.render(bottom_panel_console)


        #---------------------------------------------------------------------
        # Draw the selection cursor if in cursor input state.
        #---------------------------------------------------------------------
        if game_state == GameStates.CURSOR_INPUT:
            cursor.draw()

        #---------------------------------------------------------------------
        # Render any menus.
        #---------------------------------------------------------------------
        if game_state in INVENTORY_STATES:
            inventory_message, highlight_attr = construct_inventory_data(
                game_state)
            menu_console, menu_x, menu_y = invetory_menu(
                inventory_message, player.inventory,
                inventory_width=50,
                screen_width=SCREEN_WIDTH,
                screen_height=SCREEN_HEIGHT,
                highlight_attr=highlight_attr)

        #---------------------------------------------------------------------
        # Advance the frame of any animations.
        #---------------------------------------------------------------------
        if game_state == GameStates.ANIMATION_PLAYING:
            animation_finished = animation_player.next_frame()
            sleep(ANIMATION_INTERVAL)
            if animation_finished:
                skip_player_input = True
                game_state, previous_game_state = previous_game_state, game_state

        #---------------------------------------------------------------------
        # DEBUG
        # These switches highlight the various game state arrays.
        #---------------------------------------------------------------------
        # highlight_array(game_map.walkable, game_map, COLORS['cursor_tail'])
        # highlight_array(game_map.door, game_map, COLORS['cursor_tail'])
        # highlight_array(game_map.blocked, game_map, COLORS['cursor_tail'])
        # highlight_array(game_map.fire, game_map, COLORS['darker_red'])
        # highlight_array(game_map.steam, game_map, COLORS['desaturated_green'])
        # highlight_array(game_map.terrain, game_map, COLORS['cursor_tail'])
        # highlight_array(game_map.water, game_map, COLORS['cursor_tail'])
        highlight_stairs(game_map, COLORS['red'])
        highlight_rooms(game_map, COLORS['cursor_tail'])
        # draw_dijkstra_map_of_radius(game_map, player, radius=3)


        #---------------------------------------------------------------------
        # Blit the subconsoles to the main console and flush all rendering.
        #---------------------------------------------------------------------
        root_console.blit(game_map.console, 0, MAP_PANEL_CONFIG['y'],
                          SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        root_console.blit(top_panel_console, 0, 0,
                          SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        root_console.blit(bottom_panel_console, 0, BOTTOM_PANEL_CONFIG['y'],
                          SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        if game_state in INVENTORY_STATES:
            root_console.blit(menu_console, menu_x, menu_y,
                              SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        #---------------------------------------------------------------------
        # Clear all the entities drawn to the consoles, else we will re-draw
        # them in the same positions next game loop.
        #---------------------------------------------------------------------
        game_map.undraw_all()

        #---------------------------------------------------------------------
        # Get key input from the player.
        #---------------------------------------------------------------------
        if not skip_player_input:
            user_input = get_user_input()
            if game_state in INPUT_STATES and not user_input:
                continue
        action = player.input_handler.handle_keys(user_input, game_state)

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
        cursor_select = action.get(InputTypes.CURSOR_SELECT)
        inventory_index = action.get(InputTypes.INVENTORY_INDEX)
        move = action.get(InputTypes.MOVE)
        pickup = action.get(InputTypes.PICKUP)

        #----------------------------------------------------------------------
        # Player Move Action
        #......................................................................
        # The player has entered a move action.  Chack if the space in that
        # direction is movable, and if so put a move result on the queue.  If
        # if not, attack the blocking entity by putting an attack action on the
        # queue.
        #----------------------------------------------------------------------
        if move and game_state == GameStates.PLAYER_TURN:
            player_move_or_attack(move,
                                  player=player,
                                  game_map=game_map,
                                  player_turn_results=player_turn_results)
        #----------------------------------------------------------------------
        # Player Pickup
        #......................................................................
        # The player has attempted to pickup an item.  If there is an item in
        # the players space, put a pickup action on the queue.
        #----------------------------------------------------------------------
        elif pickup and game_state == GameStates.PLAYER_TURN:
            pickup_entity(game_map, player, player_turn_results)
        #----------------------------------------------------------------------
        # Player Inventory use / drop
        #......................................................................
        # The player has attempted to use or drop an item from the inventory.
        # Check which state we are in (using or dropping) and put an
        # instruction on the queue.
        #----------------------------------------------------------------------
        elif (game_state in INVENTORY_STATES
              and inventory_index is not None
              and inventory_index < len(player.inventory.items)
              # The inventory can be opened after the player has died, but we
              # don't want to let them use any items.
              and previous_game_state != GameStates.PLAYER_DEAD):
            item = player.inventory.items[inventory_index]
            process_selected_item(item,
                                  player=player,
                                  game_map=game_map,
                                  game_state=game_state,
                                  player_turn_results=player_turn_results)
            game_state, previous_game_state = previous_game_state, game_state

        #----------------------------------------------------------------------
        # Handle cursor movement.
        #......................................................................
        # The player is currently in cursor select mode, where they have free
        # control of a cursor to select and square within their visible range.
        #----------------------------------------------------------------------
        if move and game_state == GameStates.CURSOR_INPUT:
            cursor.move(*move)
        if cursor_select and game_state == GameStates.CURSOR_INPUT:
            player_turn_results.extend(cursor.select())
            game_state, previous_game_state = previous_game_state, game_state
            cursor = None

        #----------------------------------------------------------------------
        # Process the results stack
        #......................................................................
        # We are done processing player inputs, and may have some results on
        # the player turn stack.  Process the stack by popping off the top
        # result from the queue.  There are many different possible results,
        # so each is handled with a dedicated handler.
        #
        # Note: Handling a result may result in other results being added to
        # the stack, so we continually process the results stack until it is
        # empty.
        #----------------------------------------------------------------------
        while (game_state not in (GameStates.CURSOR_INPUT, GameStates.ANIMATION_PLAYING)
               and player_turn_results != []):

            # Sort the turn results stack by the priority order.
            player_turn_results = sorted(
                flatten_list_of_dictionaries(player_turn_results),
                key = lambda d: get_key_from_single_key_dict(d))

            result = player_turn_results.pop()
            result_type, result_data = unpack_single_key_dict(result)

            # We were in a state where player input was locked out, restore it.
            if result_type == ResultTypes.RESTORE_PLAYER_INPUT:
                skip_player_input = False
            # Play an animation.
            if result_type == ResultTypes.ANIMATION:
                animation_player = construct_animation(result_data, game_map)
                # After the animation finishes, we do not want to get input
                # from the player before continuing to process the results
                # stack, so set a flag signaling to skip this step, and then
                # push a message that will restore it once we come back to
                # continue processing the stack.
                skip_player_input = True
                player_turn_results.append(
                    {ResultTypes.RESTORE_PLAYER_INPUT: True})
                game_state, previous_game_state = (
                    GameStates.ANIMATION_PLAYING, game_state)
                break
            # Drop into cursor input mode for targeting.
            if result_type == ResultTypes.CURSOR_MODE:
                x, y, callback, mode = result_data
                cursor = Cursor(player.x, player.y, game_map,
                                callback=callback,
                                cursor_type=mode)
                game_state, previous_game_state = (
                    GameStates.CURSOR_INPUT, game_state)
                break
            # Move the player according to some user input.
            if result_type == ResultTypes.MOVE:
                player.movable.move(game_map, *result_data)
            # Find a random open position on the map, and move the player there
            # immediately.
            if result_type == ResultTypes.MOVE_TO_RANDOM_POSITION:
                entity = result_data
                position = game_map.find_random_open_position()
                entity.movable.set_position_if_able(game_map, *position)
            # Set the player's position to some given coordinates, used when
            # moving more than one step or teleporting (say, due to a raipier
            # attack or teleport staff).
            if result_type == ResultTypes.SET_POSITION:
               entity, x, y = result_data
               entity.movable.set_position_if_able(game_map, x, y)
            # Add a message to the log.
            if result_type == ResultTypes.MESSAGE:
                message_log.add_message(result_data)
            # Add an item to the inventory and remove it from the game map.
            if result_type == ResultTypes.ADD_ITEM_TO_INVENTORY:
                entity, item = result_data
                entity.inventory.add(item)
                item.commitable.delete(game_map)
            # Remove consumed items from inventory.
            if result_type == ResultTypes.DISCARD_ITEM:
                item, consumed = result_data
                if consumed:
                    player.inventory.remove(item)
            # Remove dropped items from inventory and place on the map
            if result_type == ResultTypes.DROP_ITEM_FROM_INVENTORY:
                entity, item = result_data
                entity.inventory.remove(item)
                item.x, item.y = entity.x, entity.y
                game_map.entities.append(item)
            # Process a damage message, possibly transforming it due to
            # elemental defences or other abilities.
            if result_type == ResultTypes.DAMAGE:
                process_damage(game_map, result_data, player_turn_results)
            # Commit final processed damage to an entity.
            if result_type == ResultTypes.HARM:
                process_harm(
                    game_map, result_data, player_turn_results, harmed_queue)
            # Increase the maximum HP of an entity
            if result_type == ResultTypes.INCREASE_MAX_HP:
                entity, amount = result_data
                entity.harmable.max_hp += amount
            # Increase the maximum attack power of an entity
            if result_type == ResultTypes.INCREASE_ATTACK_POWER:
                entity, amount = result_data
                entity.attacker.power += amount
            # Don defensive equipment.
            if result_type == ResultTypes.EQUIP_ARMOR:
                entity, armor = result_data
                entity_equip_armor(entity, armor, player_turn_results)
            # Don offensive equipment.
            if result_type == ResultTypes.EQUIP_WEAPON:
                entity, weapon = result_data
                entity_equip_weapon(entity, weapon, player_turn_results)
            # Remove defensive equipment.
            if result_type == ResultTypes.REMOVE_ARMOR:
                entity, armor = result_data
                entity_remove_armor(entity, armor, player_turn_results)
            # Remove offensive equipment.
            if result_type == ResultTypes.REMOVE_WEAPON:
                entity, weapon = result_data
                entity_remove_weapon(entity, weapon, player_turn_results)
            # Put an entity in a confused state
            if result_type == ResultTypes.CONFUSE:
                entity = result_data
                apply_status(
                    entity, player, PlayerConfusedManager, EnemyConfusedManager)
            if result_type == ResultTypes.DOUBLE_SPEED:
                entity = result_data
                apply_status(entity, player, SpeedManager, SpeedManager)
            # Freeze the player
            if result_type == ResultTypes.FREEZE:
                entity = result_data
                # TODO: Freezing of a player is not yet implemented.
                apply_status(entity, player, None, EnemyFrozenManager)
            # Add a new entity to the game map.
            if result_type == ResultTypes.ADD_ENTITY:
                entity = result_data
                entity.commitable.commit(game_map)
                player_turn_results.extend(encroach_on_all(entity, game_map))
            # Remove an entity from the game map.
            if result_type == ResultTypes.REMOVE_ENTITY:
                entity = result_data
                entity.commitable.delete(game_map)
            # Handle death
            if result_type == ResultTypes.DEAD_ENTITY:
                dead_entity = result_data
                if dead_entity == player:
                    player_turn_results.extend(kill_player(player))
                    game_state = GameStates.PLAYER_DEAD
                elif dead_entity:
                    player_turn_results.extend(
                        kill_monster(dead_entity, game_map))
                    make_corpse(dead_entity)
            # Handle a player death message.  Death messages are special in
            # that they immediately break out of the game loop.
            if result_type == ResultTypes.DEATH_MESSAGE:
                death_message = result_data
                message_log.add_message(death_message)
                break
            # End the player's turn
            if result_type == ResultTypes.END_TURN:
                game_turn += 1
                game_state, previous_game_state = (
                    GameStates.POST_PLAYER_TURN, game_state)


        #---------------------------------------------------------------------
        # Post player turn checks.
        #---------------------------------------------------------------------
        if game_state == GameStates.POST_PLAYER_TURN:
            # Check if the player has entered into a square containing stairs.
            # If so, end the current floor immediately.
            if (player.x, player.y) == game_map.upward_stairs_position:
                game_map.entities.remove(player)
                return FloorResultTypes.INCREMENT_FLOOR, game_turn
            if (player.x, player.y) == game_map.downward_stairs_position:
                game_map.entities.remove(player)
                return FloorResultTypes.DECREMENT_FLOOR, game_turn
            # All rechargable items get ticked.
            for item in player.inventory:
                if item.rechargeable:
                    enemy_turn_results.extend(item.rechargeable.tick())
            # All confused entities get ticked
            if player.status_manager:
                player.status_manager.tick()
            # All encroaching entities interact with their cellmates.
            enemy_turn_results.extend(encroach_on_all(player, game_map))
            # The player re-gains or loses swim stamina.
            if game_map.water[player.x, player.y]:
                enemy_turn_results.extend(player.swimmable.swim())
            else:
                enemy_turn_results.extend(player.swimmable.rest())
            # Pass the turn to the enemies.
            game_state = GameStates.ENEMY_TURN


        #-------------------------------------------------------------------
        # All enemies and terrain take thier turns.
        #-------------------------------------------------------------------
        if game_state == GameStates.ENEMY_TURN:

            for entity in (e for e in game_map.entities if e != player):
                # Enemies move and attack if possible.
                if entity.ai:
                    turn = entity.ai.take_turn(game_map)
                    enemy_turn_results.extend(turn)
                # If the enemy has a current status, tick it.
                if entity.status_manager:
                    entity.status_manager.tick()
                # Fire and gas dissipates.
                if entity.dissipatable:
                    enemy_turn_results.extend(
                        entity.dissipatable.dissipate(game_map))
                # Interact with water.
                if game_map.water[entity.x, entity.y] and entity.floatable:
                    enemy_turn_results.extend(
                        entity.floatable.float(game_map))
                if game_map.water[entity.x, entity.y] and entity.swimmable:
                    enemy_turn_results.extend(
                        entity.swimmable.swim())
                # Fire burns entities in the same space.
                if entity.entity_type == EntityTypes.FIRE:
                    burnable_entities_at_position = (
                        get_all_entities_with_component_in_position(
                            (entity.x, entity.y), game_map, "burnable"))
                    for e in burnable_entities_at_position:
                        enemy_turn_results.extend(e.burnable.burn(game_map))
                # Fire and gas spreads.
                if entity.spreadable:
                    enemy_turn_results.extend(
                        entity.spreadable.spread(game_map))
                # Steam scalds entities in the same space.
                if entity.entity_type == EntityTypes.STEAM:
                    scaldable_entities_at_position = (
                        get_all_entities_with_component_in_position(
                            (entity.x, entity.y), game_map, "scaldable"))
                    for e in scaldable_entities_at_position:
                        enemy_turn_results.extend(e.scaldable.scald(game_map))
            game_state = GameStates.PLAYER_TURN

        #---------------------------------------------------------------------
        # Process all result actions of enemy turns.
        #---------------------------------------------------------------------
        while enemy_turn_results != []:

            enemy_turn_results = sorted(
                flatten_list_of_dictionaries(enemy_turn_results),
                key = lambda d: get_key_from_single_key_dict(d))

            result = enemy_turn_results.pop()
            result_type, result_data = unpack_single_key_dict(result)

            # Handle a move action
            if result_type == ResultTypes.SET_POSITION:
                monster, x, y = result_data
                monster.movable.set_position_if_able(game_map, x, y)
            # Handle a move towards action.  Move towards a target.
            if result_type == ResultTypes.MOVE_TOWARDS:
                #import pdb; pdb.set_trace()
                monster, target_x, target_y = result_data
                monster.movable.move_towards(game_map, target_x, target_y)
            # Handle a move random adjacent action.  Move to a random adjacent
            # square.
            if result_type == ResultTypes.MOVE_RANDOM_ADJACENT:
                monster = result_data
                monster.movable.move_to_random_adjacent(game_map)
            # Handle a simple message.
            if result_type == ResultTypes.MESSAGE:
                message = result_data
                message_log.add_message(message)
            # Handle damage dealt, possibly transforming it.
            if result_type == ResultTypes.DAMAGE:
                process_damage(game_map, result_data, enemy_turn_results)
            # Commit damage to an entity.
            if result_type == ResultTypes.HARM:
                process_harm(
                    game_map, result_data, enemy_turn_results, harmed_queue)
            # Add a use to an item
            if result_type == ResultTypes.RECHARGE_ITEM:
                item = result_data
                item.consumable.uses += 1
            # Entities swim and thier stamana decreases.
            if result_type == ResultTypes.CHANGE_SWIM_STAMINA:
                entity, stamina_change = result_data
                entity.swimmable.change_stamina(stamina_change)
            # Add a new entity to the game.
            if result_type == ResultTypes.ADD_ENTITY:
                entity = result_data
                entity.commitable.commit(game_map)
            # Remove an entity from the game.
            if result_type == ResultTypes.REMOVE_ENTITY:
                entity = result_data
                entity.commitable.delete(game_map)
            # Handle death.
            if result_type == ResultTypes.DEAD_ENTITY:
                dead_entity = result_data
                if dead_entity == player:
                    enemy_turn_results.extend(kill_player(player))
                    game_state = GameStates.PLAYER_DEAD
                elif dead_entity:
                    enemy_turn_results.extend(
                        kill_monster(dead_entity, game_map))
                    make_corpse(dead_entity)


        #---------------------------------------------------------------------
        # Handle meta actions,
        #---------------------------------------------------------------------
        show_invetory = action.get(InputTypes.SHOW_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and show_invetory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        drop_inventory = action.get(InputTypes.DROP_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        throw_inventory = action.get(InputTypes.THROW_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and throw_inventory:
            previous_game_state = game_state
            game_state = GameStates.THROW_INVENTORY

        equip_inventory = action.get(InputTypes.EQUIP_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and equip_inventory:
            previous_game_state = game_state
            game_state = GameStates.EQUIP_INVENTORY

        exit = action.get(InputTypes.EXIT)
        if exit:
            if game_state == GameStates.CURSOR_INPUT:
                cursor.clear()
            if game_state in CANCEL_STATES:
                game_state, previous_game_state = (
                    previous_game_state, game_state)
            else:
                return FloorResultTypes.END_GAME, game_turn

        fullscreen = action.get(InputTypes.FULLSCREEN)
        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        #---------------------------------------------------------------------
        # If the player is dead, the game is over.
        #---------------------------------------------------------------------
        if game_state == GameStates.PLAYER_DEAD:
            continue


if __name__ == '__main__':
    main()
