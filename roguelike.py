import tdl
from time import sleep
from collections import deque

from etc.colors import COLORS, STATUS_BAR_COLORS
from etc.config import (
   SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_CONFIG, ROOM_CONFIG, TERRAIN_CONFIG,
   PANEL_CONFIG, MESSAGE_CONFIG, FOV_CONFIG, PLAYER_CONFIG, 
   ANIMATION_INTERVAL, INVENTORY_WIDTH, SHIMMER_INTERVAL)
from etc.enum import (
    EntityTypes, GameStates, ItemTargeting, RenderOrder, Animations,
    ResultTypes, Elements)

from animations.animations import construct_animation
from components.attacker import Attacker
from components.burnable import AliveBurnable
from components.damage_transformers.defensive_transformers import (
    ElementalTransformer)
from components.equipment import Equipment
from components.harmable import Harmable
from components.inventory import Inventory
from components.movable import Movable
from components.scaldable import AliveScaldable
from components.swimmable import Swimmable
from game_objects.items import (
    HealthPotion, MagicMissileScroll, FireblastScroll, ThrowingKnife)
from game_objects.armor import LeatherArmor
from generation.floor import make_floor
from generation.item_groups import ITEM_SCHEDULE, ITEM_GROUPS
from generation.monster_groups import MONSTER_SCHEDULE, MONSTER_GROUPS
from generation.spawn_entities import spawn_entities
from generation.terrain import add_random_terrain

from cursor import Cursor
from death_functions import kill_monster, kill_player, make_corpse
from entity import Entity, get_blocking_entity_at_location
from input_handlers import handle_keys
from map import GameMap
from menus import invetory_menu
from messages import Message, MessageLog
from status_bar import StatusBar


def main():

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    # Setup playscreen with two consoles:
    #  - A place to draw the playscreen with the map and entities.
    #  - A console with the player's health bar, and a message log.
    root_console = tdl.init(
       SCREEN_WIDTH, SCREEN_HEIGHT,
       title='Roguelike Tutorial Game')
    map_console = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    panel_console = tdl.Console(SCREEN_WIDTH, PANEL_CONFIG['height'])
    message_log = MessageLog(MESSAGE_CONFIG)

    # This is you.  Kill some Orcs.
    player = Entity(0, 0, PLAYER_CONFIG["char"], 
                    COLORS[PLAYER_CONFIG["color"]], 
                    PLAYER_CONFIG["name"],
                    blocks=True,
                    render_order=RenderOrder.ACTOR,
                    attacker=Attacker(power=PLAYER_CONFIG["power"]),
                    harmable=Harmable(
                        hp=PLAYER_CONFIG["hp"],
                        defense=PLAYER_CONFIG["defense"]),
                    equipment=Equipment(),
                    movable=Movable(),
                    burnable=AliveBurnable(),
                    scaldable=AliveScaldable(),
                    swimmable=Swimmable(PLAYER_CONFIG["swim_stamina"]),
                    inventory=Inventory(PLAYER_CONFIG["inventory_size"]))
    entities = [player]

    # Setup Initial Inventory, for testing.
    player.inventory.extend([HealthPotion.make(0, 0) for _ in range(3)])
    player.inventory.extend([ThrowingKnife.make(0, 0) for _ in range(3)])
    player.inventory.extend([MagicMissileScroll.make(0, 0) for _ in range(3)])
    player.inventory.extend([FireblastScroll.make(0, 0) for _ in range(3)])

    # Generate the map and place player, monsters, and items.
    floor = make_floor(FLOOR_CONFIG, ROOM_CONFIG)
    game_map = GameMap(floor, map_console)
    terrain = add_random_terrain(game_map, entities, TERRAIN_CONFIG)
    game_map.place_player(player)
    spawn_entities(MONSTER_SCHEDULE, MONSTER_GROUPS, game_map, entities)
    spawn_entities(ITEM_SCHEDULE, ITEM_GROUPS, game_map, entities)

    #-------------------------------------------------------------------------
    # Game State Varaibles
    #-------------------------------------------------------------------------
    # Counter for the game loop iteration we are on.
    game_loop = -1
    # Initial values for game states
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    # Used for control flow after and animation.
    skip_player_input = False
    # We only want to recompute the fov when needed.  For example, if the
    # player just used an item and has not moved, the fov will be the same.
    fov_recompute = True
    # Data needed to play an animation.
    animation_player = None
    # A queue for storing enemy targets that have taken damage.  Used to render
    # enemy health bars in the UI.
    harmed_queue = deque(maxlen=3)
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

        game_loop += 1

        #---------------------------------------------------------------------
        # Game loop variables
        #---------------------------------------------------------------------
        user_input = None

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
        # Shimmer the colors of entities that shimmer.
        #---------------------------------------------------------------------
        if game_loop % SHIMMER_INTERVAL == 0:
            for entity in entities:
                if entity.shimmer:
                    entity.shimmer.shimmer()

        #---------------------------------------------------------------------
        # Render and display the dungeon and its inhabitates.
        #---------------------------------------------------------------------
        game_map.update_and_draw_all(entities, fov_recompute)

        #---------------------------------------------------------------------
        # Render the UI
        #---------------------------------------------------------------------
        panel_console.clear(fg=COLORS['white'], bg=COLORS['black'])
        player.harmable.render_status_bar(panel_console, 1, 1)
        player.swimmable.render_status_bar(panel_console, 1, 3)
        message_log.render(panel_console)
        for idx, entity in enumerate(harmed_queue):
            entity.harmable.render_status_bar(
                panel_console, PANEL_CONFIG['bar_width'] + 2, 2*idx + 1)

        #---------------------------------------------------------------------
        # Draw the selection cursor if in cursor input state.
        #---------------------------------------------------------------------
        if game_state == GameStates.CURSOR_INPUT:
            cursor.draw()

        #---------------------------------------------------------------------
        # Render any menus.
        #---------------------------------------------------------------------
        menu_states = (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                       GameStates.THROW_INVENTORY, GameStates.EQUIP_INVENTORY)
        if game_state in menu_states:
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
        # Blit the subconsoles to the main console and flush all rendering.
        #---------------------------------------------------------------------
        root_console.blit(game_map.console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        root_console.blit(panel_console, 0, PANEL_CONFIG['y'],
                          SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                          GameStates.THROW_INVENTORY, GameStates.EQUIP_INVENTORY):
            root_console.blit(menu_console, menu_x, menu_y,
                              SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        #---------------------------------------------------------------------
        # Clear all the entities drawn to the consoles, else we will re-draw
        # them in the same positions next game loop.
        #---------------------------------------------------------------------
        game_map.undraw_all(entities)

        #---------------------------------------------------------------------
        # Get key input from the player.
        #---------------------------------------------------------------------
        input_states = (
            GameStates.PLAYER_TURN, GameStates.SHOW_INVENTORY,
            GameStates.DROP_INVENTORY, GameStates.THROW_INVENTORY,
            GameStates.EQUIP_INVENTORY, GameStates.CURSOR_INPUT,
            GameStates.PLAYER_DEAD)
        if not skip_player_input:
            user_input = get_user_input()
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
        # Unless the player moves, we do not need to recompute the fov.
        fov_recompute = False
        if move and game_state == GameStates.PLAYER_TURN:
            player_move_or_attack(move, 
                                  player=player, 
                                  entities=entities, 
                                  game_map=game_map, 
                                  player_turn_results=player_turn_results)
            game_state = GameStates.ENEMY_TURN
        #----------------------------------------------------------------------
        # Player Pickup
        #......................................................................
        # The player has attempted to pickup an item.  If there is an item in
        # the players space, put a pickup action on the queue.
        #----------------------------------------------------------------------
        elif pickup and game_state == GameStates.PLAYER_TURN:
            # TODO: Create pickup_entity function.
            for entity in entities:
                if (entity.pickupable
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
                             GameStates.THROW_INVENTORY, GameStates.EQUIP_INVENTORY)
            and inventory_index is not None
            and inventory_index < len(player.inventory.items)
            and previous_game_state != GameStates.PLAYER_DEAD):

            item = player.inventory.items[inventory_index]
            process_selected_item(item, 
                                  player=player,
                                  entities=entities,
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
        while game_state != GameStates.ANIMATION_PLAYING and player_turn_results != []:

            result = player_turn_results.pop()

            print()
            print("Player turn.")
            print(result)

            animation = result.get(ResultTypes.ANIMATION)
            cursor_mode = result.get(ResultTypes.CURSOR_MODE)
            damage = result.get(ResultTypes.DAMAGE)
            dead_entity = result.get(ResultTypes.DEAD_ENTITY)
            death_message = result.get(ResultTypes.DEATH_MESSAGE)
            equip_armor = result.get(ResultTypes.EQUIP_ARMOR)
            heal = result.get(ResultTypes.HEAL)
            item_added = result.get(ResultTypes.ITEM_ADDED)
            item_consumed = result.get(ResultTypes.ITEM_CONSUMED)
            item_dropped = result.get(ResultTypes.ITEM_DROPPED)
            message = result.get(ResultTypes.MESSAGE)
            move = result.get(ResultTypes.MOVE)
            new_entity = result.get(ResultTypes.ADD_ENTITY)
            remove_armor = result.get(ResultTypes.REMOVE_ARMOR)
            remove_entity = result.get(ResultTypes.REMOVE_ENTITY)
            restore_player_input = result.get(ResultTypes.RESTORE_PLAYER_INPUT)

            # Play an animation.
            if restore_player_input:
                skip_player_input = False
            if animation:
                animation_player = construct_animation(
                    animation, game_map, player=player)
                # We want to play the animiation immediately, and then continue
                # to process everything else after it completes.  So remove the
                # enimation data from teh results structure, and push the rest
                # back on top of the stack.
                result.pop(ResultTypes.ANIMATION)
                player_turn_results.append(result)
                skip_player_input = True
                player_turn_results.append(
                    {ResultTypes.RESTORE_PLAYER_INPUT: True})
                game_state, previous_game_state = (
                    GameStates.ANIMATION_PLAYING, game_state)
                break
            # Move the player.
            if move:
                player.movable.move(game_map, *move)
                fov_recompute = True
            # Add to the message log.
            if message:
                message_log.add_message(message)
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
            # Damage an entity.
            if damage:
                target, amount, element = damage
                damage_result = target.harmable.harm(
                    game_map, amount, element)
                enemy_turn_results.extend(damage_result)
                if target not in harmed_queue:
                    harmed_queue.appendleft(target)
            # Heal an entity
            if heal:
                target, amount = heal
                target.harmable.heal(amount)
            # Don defensive equipment.
            if equip_armor:
                entity, armor = equip_armor
                # TODO: Factor out as equip_armor
                if not hasattr(entity, "harmable"):
                    raise AttributeError(
                        "Non harmable entities cannot equip Armor")
                if entity.equipment.armor or armor.equipable.equipped:
                    player_turn_results.append({
                        ResultTypes.MESSAGE: Message(
                            f"{entity.name} cannot equip {armor.name}",
                            COLORS['white'])})
                else:
                    entity.equipment.armor = armor
                    armor.equipable.equipped = True
                    entity.harmable.add_damage_transformers(
                        armor.equipable.damage_transformers)
                    player_turn_results.append({
                        ResultTypes.MESSAGE: Message(
                            f"{entity.name} equipped {armor.name}",
                            COLORS['white'])})
            # Remove defensive equipment.
            if remove_armor:
                entity, armor = remove_armor
                if not hasattr(entity, "harmable"):
                    raise AttributeError(
                        "Non harmable entities cannot un-equip Armor")
                if not entity.equipment.armor or not armor.equipable.equipped:
                    player_turn_results.append({
                        ResultTypes.MESSAGE: Message(
                            f"{entity.name} cannot un-equip {armor.name}",
                            COLORS['white'])})
                else:
                    entity.equipment.armor = None
                    armor.equipable.equipped = False
                    entity.harmable.remove_damage_transformers(
                        armor.equipable.damage_transformers)
                    player_turn_results.append({
                        ResultTypes.MESSAGE: Message(
                            f"{entity.name} removed {armor.name}",
                            COLORS['white'])})
            # Add a new entity to the game.
            if new_entity:
                entity = new_entity
                if not game_map.blocked[entity.x, entity.y]:
                    game_map.blocked[entity.x, entity.y] = True
                    entities.append(entity)
            # Remove an entity from the game.
            if remove_entity:
                entity = remove_entity
                entities.remove(entity)
            # Handle death
            if dead_entity == player:
                player_turn_results.extend(kill_player(player))
                game_state = GameStates.PLAYER_DEAD
            elif dead_entity:
                player_turn_results.extend(
                    kill_monster(dead_entity, game_map))
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
                    player.x, player.y, game_map, callback=callback)
                game_state, previous_game_state = (
                    GameStates.CURSOR_INPUT, game_state)

        #---------------------------------------------------------------------
        # Post player turn checks.
        #---------------------------------------------------------------------
        # If the player is swimming, decrease the swim stamina.  Otherwise,
        # recover swim stamina.
        if game_state == GameStates.ENEMY_TURN:
            if game_map.water[player.x, player.y]:
                enemy_turn_results.extend(player.swimmable.swim())
            else:
                enemy_turn_results.extend(player.swimmable.rest())

        #---------------------------------------------------------------------
        # All enemies and hazardous terrain and entities take thier turns.
        #---------------------------------------------------------------------
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                # Enemies move and attack if possible.
                if entity.ai:
                    enemy_turn_results.extend(entity.ai.take_turn(
                        player, game_map))
                # Fire and gas spreads.
                if entity.spreadable:
                    enemy_turn_results.extend(
                        entity.spreadable.spread(game_map, entities))
                # Fire and gas dissipates.
                if entity.dissipatable:
                    enemy_turn_results.extend(
                        entity.dissipatable.dissipate(game_map))
                # Fire burns entities in the same space.
                if entity.entity_type == EntityTypes.FIRE:
                    burnable_entities_at_position = (
                        entity.get_all_entities_with_component_in_same_position(
                            entities, "burnable"))
                    for e in burnable_entities_at_position:
                        enemy_turn_results.extend(e.burnable.burn(game_map))
                # Steam scalds entities in the same space.
                if entity.entity_type == EntityTypes.STEAM:
                    scaldable_entities_at_position = (
                        entity.get_all_entities_with_component_in_same_position(
                            entities, "scaldable"))
                    for e in scaldable_entities_at_position:
                        enemy_turn_results.extend(e.scaldable.scald(game_map))
            game_state = GameStates.PLAYER_TURN

        #---------------------------------------------------------------------
        # Process all result actions of enemy turns.
        #---------------------------------------------------------------------
        while enemy_turn_results != []:
            result = enemy_turn_results.pop()

            change_swim_stamina = result.get(ResultTypes.CHANGE_SWIM_STAMINA)
            damage = result.get(ResultTypes.DAMAGE)
            dead_entity = result.get(ResultTypes.DEAD_ENTITY)
            message = result.get(ResultTypes.MESSAGE)
            move_random_adjacent = result.get(ResultTypes.MOVE_RANDOM_ADJACENT)
            move_towards = result.get(ResultTypes.MOVE_TOWARDS)
            new_entity = result.get(ResultTypes.ADD_ENTITY)
            remove_entity = result.get(ResultTypes.REMOVE_ENTITY)

            # Handle a move towards action.  Move towards a target.
            if move_towards:
               monster, target_x, target_y = move_towards
               monster.movable.move_towards(target_x, target_y, game_map, entities)
            # Handle a move random adjacent action.  Move to a random adjacent
            # square.
            if move_random_adjacent:
               monster = move_random_adjacent
               monster.movable.move_to_random_adjacent(game_map, entities)
            # Handle a simple message.
            if message:
                message_log.add_message(message)
            # Handle damage dealt.
            if damage:
                target, amount, element = damage
                damage_result = target.harmable.harm(
                    game_map, amount, element)
                enemy_turn_results.extend(damage_result)
                if target != player and target not in harmed_queue:
                    harmed_queue.appendleft(target)
            # Entities swim and thier stamana decreases.
            if change_swim_stamina:
                entity, stamina_change = change_swim_stamina
                entity.swimmable.change_stamina(stamina_change) 
            # Add a new entity to the game.
            if new_entity:
                entity = new_entity
                if not game_map.blocked[entity.x, entity.y]:
                    game_map.blocked[entity.x, entity.y] = True
                    entities.append(entity)
            # Remove an entity from the game.
            if remove_entity:
                entity = remove_entity
                # For example: different fires can spread to the same space in
                # one turn, which results in two requests to remove grass in
                # that space.
                if entity in entities:
                    entities.remove(entity)
            # Handle death.
            if dead_entity == player:
                enemy_turn_results.extend(kill_player(player, COLORS))
                game_state = GameStates.PLAYER_DEAD
            elif dead_entity:
                enemy_turn_results.extend(
                    kill_monster(dead_entity, game_map))
                dead_entities.append(dead_entity)

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

        equip_inventory = action.get(ResultTypes.EQUIP_INVENTORY)
        if game_state == GameStates.PLAYER_TURN and equip_inventory:
            previous_game_state = game_state
            game_state = GameStates.EQUIP_INVENTORY

        exit = action.get(ResultTypes.EXIT)
        if exit:
            if game_state == GameStates.CURSOR_INPUT:
                cursor.clear()
            if game_state in (
                GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                GameStates.THROW_INVENTORY, GameStates.EQUIP_INVENTORY,
                GameStates.CURSOR_INPUT):
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
        # If the last turn resulted in a dead monster: 
        #   - Draw it as a corpse.
        #   - Replace all is components with null components.
        #   - Remove it from the harmed_queue so that its health bars will not
        #     render.
        #
        # Note we do not do this until *after* an animation is finished, since
        # the game state will possibly already know the monster is dead before
        # playing the animation.
        #---------------------------------------------------------------------
        if game_state != GameStates.ANIMATION_PLAYING:
            while dead_entities:
                dead_entity = dead_entities.pop()
                while dead_entity in harmed_queue:
                    harmed_queue.remove(dead_entity)
                make_corpse(dead_entity)

        #---------------------------------------------------------------------
        # If the player is dead, the game is over.
        #---------------------------------------------------------------------
        if game_state == GameStates.PLAYER_DEAD:
            continue


def construct_inventory_data(game_state):
    if game_state == GameStates.SHOW_INVENTORY:
        invetory_message = "Press the letter next to the item to use it.\n"
        highlight_attr = "usable"
    elif game_state == GameStates.DROP_INVENTORY:
        invetory_message = "Press the letter next to the item to drop it.\n"
        highlight_attr = None
    elif game_state == GameStates.THROW_INVENTORY:
        invetory_message = "Press the letter next to the item to throw it.\n"
        highlight_attr = "throwable"
    elif game_state == GameStates.EQUIP_INVENTORY:
        invetory_message = "Press the letter next to the item to equip it.\n"
        highlight_attr = "equipable"
    return invetory_message, highlight_attr

def get_user_input():
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            break
    else:
        user_input = None
    return user_input

def process_selected_item(item, *,
                          player=None,
                          entities=None,
                          game_state=None,
                          game_map=None, 
                          player_turn_results=None): 
    if game_state == GameStates.SHOW_INVENTORY:
        if item.usable:
            player_turn_results.extend(item.usable.use(game_map, player, entities))
    elif game_state == GameStates.THROW_INVENTORY:
        if item.throwable:
            player_turn_results.extend(item.throwable.throw(game_map, player, entities))
    elif game_state == GameStates.EQUIP_INVENTORY:
        if item.equipable and item.equipable.equipped:
            player_turn_results.extend(item.equipable.remove(player))
        elif item.equipable:
            player_turn_results.extend(item.equipable.equip(player))
    elif game_state == GameStates.DROP_INVENTORY:
        player_turn_results.extend(player.inventory.drop(item))

def player_move_or_attack(move, *,
                          player=None, 
                          entities=None, 
                          game_map=None,
                          player_turn_results=None):
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


if __name__ == '__main__':
    main()
