import tdl
from time import sleep

from etc.colors import COLORS
from etc.config import (
   SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_CONFIG, ROOM_CONFIG,
   PANEL_CONFIG, MESSAGE_CONFIG, FOV_CONFIG)
from etc.enum import (
    EntityTypes, GameStates, ItemTargeting, RenderOrder, Animations, 
    ResultTypes)

from components.attacker import Attacker
from components.harmable import Harmable
from components.inventory import Inventory
from map.map import GameMap
from map.floor import make_floor
from spawnable.monsters import MONSTER_SCHEDULE, MONSTER_GROUPS
from spawnable.items import ITEM_SCHEDULE, ITEM_GROUPS
from spawnable.spawnable import spawn_entities
from spawnable.items import (
    HealthPotion, MagicMissileScroll, FireblastScroll, ThrowingKnife)
from animations.animations import construct_animation

from cursor import Cursor
from input_handlers import handle_keys
from messages import Message, MessageLog
from entity import Entity, get_blocking_entity_at_location
from menus import invetory_menu
from death_functions import kill_monster, kill_player, make_corpse
from rendering import (
    clear_all, render_all, render_health_bars, render_messages)


def main():

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    # Setup playscreen with two consoles:
    #  - A place to draw the playscreen with the map and entities.
    #  - A console with the player's health bar, and a message log.
    root_console = tdl.init(
       SCREEN_WIDTH, SCREEN_HEIGHT,
       title='Rougelike Tutorial Game')
    map_console = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    panel_console = tdl.Console(SCREEN_WIDTH, PANEL_CONFIG['height'])
    message_log = MessageLog(MESSAGE_CONFIG)

    # This is you.  Kill some Orcs.
    player = Entity(0, 0, '@', COLORS['white'], 'Player', 
                    blocks=True,
                    render_order=RenderOrder.ACTOR,
                    attacker=Attacker(power=5),
                    harmable=Harmable(hp=2000, defense=2),
                    inventory=Inventory(26))
    entities = [player]

    # Setup Initial Inventory, for testing.
    player.inventory.extend([HealthPotion.make(0, 0) for _ in range(3)])
    player.inventory.extend([ThrowingKnife.make(0, 0) for _ in range(3)])
    player.inventory.extend([MagicMissileScroll.make(0, 0) for _ in range(3)])
    player.inventory.extend([FireblastScroll.make(0, 0) for _ in range(3)])
 
    # Generate the map and place player, monsters, and items.
    game_map = GameMap(FLOOR_CONFIG['width'], FLOOR_CONFIG['height'])
    floor = make_floor(FLOOR_CONFIG, ROOM_CONFIG)
    floor.place_player(player)
    floor.write_to_game_map(game_map)
    spawn_entities(MONSTER_SCHEDULE, MONSTER_GROUPS, floor, entities)
    spawn_entities(ITEM_SCHEDULE, ITEM_GROUPS, floor, entities)
    

    #-------------------------------------------------------------------------
    # Game State Varaibles
    #-------------------------------------------------------------------------
    # Initial values for game states
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    # We only want to recompute the fov when needed.  For example, if the
    # player just used an item and has not moved, the fov will be the same.
    fov_recompute = True
    # Data needed to play an animation.
    animation_player = None
    # A cursor object for allowing the user to select a space on the map.
    cursor = None
    # A list of recently dead enemies.  We need this to defer drawing thier
    # corpses until *after* any animations have finished.
    dead_entities = []
    # Stacks for holding the results of player and enemy turns.
    player_turn_results = []
    enemy_turn_results = []


    #-------------------------------------------------------------------------
    # Main Game Loop.
    #-------------------------------------------------------------------------
    while not tdl.event.is_window_closed():

        #---------------------------------------------------------------------
        # If needed, recompute the player's field of view.
        #---------------------------------------------------------------------
        if fov_recompute:
            game_map.compute_fov(
                player.x, player.y,
                fov=FOV_CONFIG["algorithm"],
                radius=FOV_CONFIG["radius"],
                light_walls=FOV_CONFIG["light_walls"])

        #---------------------------------------------------------------------
        # Draw the selection cursor if in cursor input state.
        #---------------------------------------------------------------------
        if game_state == GameStates.CURSOR_INPUT:
            cursor.draw()

        #---------------------------------------------------------------------
        # Render and display the dungeon and its inhabitates.
        #---------------------------------------------------------------------
        render_all(map_console, entities, game_map, fov_recompute, COLORS)
        render_health_bars(panel_console, player, PANEL_CONFIG, COLORS)
        render_messages(panel_console, message_log)

        #---------------------------------------------------------------------
        # Render any menus.
        #---------------------------------------------------------------------
        menu_states = (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, 
                       GameStates.THROW_INVENTORY)
        if game_state in menu_states:
            if game_state == GameStates.SHOW_INVENTORY:
                invetory_message = "Press the letter next to the item to use it.\n"
                highlight_attr = None
            elif game_state == GameStates.DROP_INVENTORY:
                invetory_message = "Press the letter next to the item to drop it.\n"
                highlight_attr = None
            elif game_state == GameStates.THROW_INVENTORY:
                invetory_message = "Press the letter next to the item to throw it.\n"
                highlight_attr = "throwable"
            menu_console, menu_x, menu_y = invetory_menu(
                invetory_message, player.inventory, 
                # TODO: Remove this magic number.
                inventory_width=50,
                screen_width=SCREEN_WIDTH, 
                screen_height=SCREEN_HEIGHT,
                highlight_attr=highlight_attr)

        #---------------------------------------------------------------------
        # Advance the frame of any animations.
        #---------------------------------------------------------------------
        if game_state == GameStates.ANIMATION_PLAYING:
            # Now play the animatin
            animation_finished = animation_player.next_frame()
            sleep(0.1)
            if animation_finished:
                game_state, previous_game_state = previous_game_state, game_state

        #---------------------------------------------------------------------
        # Blit the subconsoles to the main console and flush all rendering.
        #---------------------------------------------------------------------
        root_console.blit(map_console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        root_console.blit(panel_console, 0, PANEL_CONFIG['y'],
                          SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, 
                          GameStates.THROW_INVENTORY):
            root_console.blit(menu_console, menu_x, menu_y,
                              SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        # Clear all the entities drawn to the consoles, else we will re-draw
        # them in the same positions next game loop.
        clear_all(map_console, entities)

        # Unless the player moves, we do not need to recompute the fov.
        fov_recompute = False 

        #---------------------------------------------------------------------
        # Get key input from the player.
        #---------------------------------------------------------------------
        input_states = (
            GameStates.PLAYER_TURN, GameStates.SHOW_INVENTORY,
            GameStates.DROP_INVENTORY, GameStates.THROW_INVENTORY, 
            GameStates.CURSOR_INPUT)
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        if game_state in input_states and not user_input:
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
        cursor_select = action.get(ResultTypes.CURSOR_SELECT)
        inventory_index = action.get(ResultTypes.INVENTORY_INDEX)
        move = action.get(ResultTypes.MOVE)
        pickup = action.get(ResultTypes.PICKUP)

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
                    attack_results = player.attacker.attack(blocker)
                    player_turn_results.extend(attack_results)
                else:
                    player_turn_results.append({ResultTypes.MOVE: (dx, dy)})
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
                    ResultTypes.MESSAGE: Message("There is nothing to pick up!")})
            game_state = GameStates.ENEMY_TURN
        #----------------------------------------------------------------------
        # Player Inventory use / drop
        #......................................................................
        # The player has attempted to use or drop an item from the inventory.
        # Check which state we are in (using or dropping) and put an
        # instruction on the queue.
        #----------------------------------------------------------------------
        elif (game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                             GameStates.THROW_INVENTORY)
            and inventory_index is not None
            and inventory_index < len(player.inventory.items)
            and previous_game_state != GameStates.PLAYER_DEAD):
            entity = player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                if entity.item.targeting == ItemTargeting.PLAYER:
                    player_turn_results.extend(
                        entity.item.use(player))
                if entity.item.targeting == ItemTargeting.CLOSEST_MONSTER:
                    player_turn_results.extend(
                        entity.item.use(player, entities))
                if entity.item.targeting == ItemTargeting.WITHIN_RADIUS:
                    player_turn_results.extend(
                        entity.item.use(player, entities))
                if entity.item.targeting == ItemTargeting.FIRST_ALONG_PATH_TO_CURSOR:
                    player_turn_results.extend(
                        entity.item.use(game_map, player, entities))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop(entity))
            elif game_state == GameStates.THROW_INVENTORY:
                if entity.item.throwable:
                    player_turn_results.extend(
                        entity.item.throw(game_map, player, entities))
                else:
                    message = Message(
                        "You cannot throw the {}".format(entity.name),
                        COLORS['white'])
                    player_turn_results.append({ResultTypes.MESSAGE: message})
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
        while game_state != GameStates.ANIMATION_PLAYING and player_turn_results != []:
            result = player_turn_results.pop()

            animation = result.get(ResultTypes.ANIMATION)
            cursor_mode = result.get(ResultTypes.CURSOR_MODE)
            damage = result.get(ResultTypes.DAMAGE)
            dead_entity = result.get(ResultTypes.DEAD_ENTITY)
            death_message = result.get(ResultTypes.DEATH_MESSAGE)
            heal = result.get(ResultTypes.HEAL)
            item_added = result.get(ResultTypes.ITEM_ADDED)
            item_consumed = result.get(ResultTypes.ITEM_CONSUMED)
            item_dropped = result.get(ResultTypes.ITEM_DROPPED)
            message = result.get(ResultTypes.MESSAGE)
            move = result.get(ResultTypes.MOVE)

            # Move the player.
            if move:
                player.move(*move)
                fov_recompute = True
            # Add to the message log.
            if message:
                message_log.add_message(message)
            # Handle damage dealt.
            if damage:
                target, amount = damage
                damage_result = target.harmable.take_damage(amount)
                player_turn_results.extend(damage_result)
            # Add an item to the inventory.
            if item_added:
                player.inventory.add(item_added)
                entities.remove(item_added)
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
                # TODO: This calculation should not go here.
                target.harmable.hp += min(
                    amount, target.harmable.max_hp - target.harmable.hp)
            # Handle death
            if dead_entity == player:
                player_turn_results.extend(kill_player(player, COLORS))
                game_state = GameStates.PLAYER_DEAD 
            elif dead_entity:
                player_turn_results.extend(
                    kill_monster(dead_entity, COLORS))
                dead_entities.append(dead_entity)
            # Handle a player death message.  Death messages are special in
            # that they immediately break out of the game loop.
            if death_message:
                message_log.add_message(death_message)
                break
            # Enter cursor select mode.
            if cursor_mode:
                x, y, callback = cursor_mode
                cursor = Cursor(
                    player.x, player.y, map_console, game_map, 
                    callback=callback)
                game_state, previous_game_state = (
                    GameStates.CURSOR_INPUT, game_state)
            # Play an animation.
            # TODO: Factor this out into its own function. This should be easy,
            #       you only need the animation object.
            if animation:
                animation_player = construct_animation(animation, map_console, game_map)
                game_state, previous_game_state = (
                    GameStates.ANIMATION_PLAYING, game_state)
                # Immediately play the animation.
                #break

        #---------------------------------------------------------------------
        # All enemies take thier turns.
        #---------------------------------------------------------------------
        if game_state == GameStates.ENEMY_TURN:
            for entity in (x for x in entities if x.ai):
                enemy_turn_results.extend(entity.ai.take_turn(
                    player, game_map))
            game_state = GameStates.PLAYER_TURN

        #---------------------------------------------------------------------
        # Process all result actions of enemy turns.
        #---------------------------------------------------------------------
        while enemy_turn_results != []:
            result = enemy_turn_results.pop()
            move_towards = result.get('move_towards')
            move_random_adjacent = result.get('move_random_adjacent')
            message = result.get(ResultTypes.MESSAGE)
            damage = result.get(ResultTypes.DAMAGE)
            dead_entity = result.get(ResultTypes.DEAD_ENTITY)
            # Handle a move towards action.  Move towards a target.
            if move_towards:
               monster, target_x, target_y = move_towards
               monster.move_towards(target_x, target_y, game_map, entities)
            # Handle a move random adjacent action.  Move to a random adjacent
            # square.
            if move_random_adjacent:
               monster = move_random_adjacent
               monster.move_to_random_adjacent(game_map, entities)
            # Handle a simple message.
            if message:
                message_log.add_message(message)
            # Handle damage dealt.
            if damage:
                target, amount = damage
                damage_result = target.harmable.take_damage(amount)
                enemy_turn_results.extend(damage_result)
            # Handle death.
            if dead_entity == player:
                enemy_turn_results.extend(kill_player(player, COLORS))
                game_state = GameStates.PLAYER_DEAD 
            elif dead_entity:
                enemy_turn_results.extend(
                    kill_monster(dead_entity, COLORS))

        #---------------------------------------------------------------------
        # Handle meta actions,
        #---------------------------------------------------------------------
        show_invetory = action.get(ResultTypes.SHOW_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and show_invetory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        drop_inventory = action.get(ResultTypes.DROP_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        throw_inventory = action.get(ResultTypes.THROW_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and throw_inventory:
            previous_game_state = game_state
            game_state = GameStates.THROW_INVENTORY

        exit = action.get(ResultTypes.EXIT)
        if exit:
            if game_state == GameStates.CURSOR_INPUT:
                cursor.clear()
            if game_state in (
                GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                GameStates.THROW_INVENTORY, GameStates.CURSOR_INPUT):
                game_state, previous_game_state = (
                    previous_game_state, game_state)
            else:
                # Hard exit the game.
                return True

        #---------------------------------------------------------------------
        # Toggle fullscreen mode.
        #---------------------------------------------------------------------
        fullscreen = action.get(ResultTypes.FULLSCREEN)
        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        #---------------------------------------------------------------------
        # Once an animation is finished that results in a dead monster, draw it
        # as a corpse.
        #---------------------------------------------------------------------
        if game_state != GameStates.ANIMATION_PLAYING:
            while dead_entities:
                dead_entity = dead_entities.pop()
                make_corpse(dead_entity, COLORS)

        #---------------------------------------------------------------------
        # If the player is dead, the game is over.
        #---------------------------------------------------------------------
        if game_state == GameStates.PLAYER_DEAD:
            continue


if __name__ == '__main__':
    main()
