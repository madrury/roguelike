import tdl

from components.attacker import Attacker
from components.burnable import AliveBurnable
from components.defender import Defender
from components.equipment import Equipment
from components.harmable import Harmable
from components.inventory import Inventory
from components.input_handler import PlayerInputHandler
from components.movable import Movable
from components.scaldable import AliveScaldable
from components.swimmable import PlayerSwimmable

from etc.colors import COLORS
from etc.config import GLOBAL_FLOOR_CONFIG, PLAYER_CONFIG
from etc.enum import RenderOrder, GameStates, ResultTypes

from generation.floor import make_floor
from generation.item_groups import ITEM_GROUPS
from generation.monster_groups import MONSTER_GROUPS
from generation.spawn_entities import spawn_entities
from generation.terrain import add_random_terrain

from utils.utils import (
    get_blocking_entity_in_position,
    get_all_entities_with_component_in_position)

from entity import Entity
from map import GameMap
from messages import Message


def create_map(map_console, *,
               floor_schedule,
               terrain_schedule,
               monster_schedule,
               item_schedule):
    """Construct and return the game map.

    The game map is the main object representing the state of the game.
    """
    floor = make_floor(GLOBAL_FLOOR_CONFIG, floor_schedule)
    game_map = GameMap(floor, map_console)
    terrain = add_random_terrain(game_map, terrain_schedule)
    # TODO: game_map should be the first argument here.
    spawn_entities(monster_schedule, MONSTER_GROUPS, game_map)
    spawn_entities(item_schedule, ITEM_GROUPS, game_map)
    return game_map


def create_player(game_map):
    """Create the player entity and place on the game map."""
    from game_objects.items import (
        HealthPotion, MagicMissileScroll, FireblastScroll, SpeedPotion,
        TeleportationPotion, ThrowingKnife, Torch, FireStaff, IceStaff,
        ConfusionPotion)
    from game_objects.weapons import Raipier
    # This is you.  Kill some Orcs.
    player = Entity(0, 0, PLAYER_CONFIG["char"],
                    COLORS[PLAYER_CONFIG["color"]],
                    PLAYER_CONFIG["name"],
                    blocks=True,
                    render_order=RenderOrder.ACTOR,
                    attacker=Attacker(power=PLAYER_CONFIG["power"]),
                    burnable=AliveBurnable(),
                    defender=Defender(),
                    equipment=Equipment(),
                    harmable=Harmable(
                        hp=PLAYER_CONFIG["hp"],
                        defense=PLAYER_CONFIG["defense"]),
                    input_handler=PlayerInputHandler(),
                    inventory=Inventory(PLAYER_CONFIG["inventory_size"]),
                    movable=Movable(),
                    scaldable=AliveScaldable(),
                    swimmable=PlayerSwimmable(PLAYER_CONFIG["swim_stamina"]))
    # Setup Initial Inventory, for testing.
    player.inventory.extend([HealthPotion.make(0, 0) for _ in range(3)])
    player.inventory.extend([ConfusionPotion.make(0, 0)])
    player.inventory.extend([SpeedPotion.make(0, 0)])
    player.inventory.extend([TeleportationPotion.make(0, 0)])
    player.inventory.extend([ThrowingKnife.make(0, 0)])
    player.inventory.extend([MagicMissileScroll.make(0, 0)])
    player.inventory.extend([FireblastScroll.make(0, 0)])
    player.inventory.extend([Torch.make(0, 0)])
    player.inventory.extend([Raipier.make(0, 0)])
    player.inventory.extend([FireStaff.make(0, 0)])
    player.inventory.extend([IceStaff.make(0, 0)])
    return player


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
                          game_map=None,
                          game_state=None,
                          player_turn_results=None):
    # Check which inventory screen we are on and call the appropriate method.
    if game_state == GameStates.SHOW_INVENTORY:
        if item.usable:
            player_turn_results.extend(item.usable.use(game_map, player))
            player_turn_results.extend(item.consumable.consume())
    elif game_state == GameStates.THROW_INVENTORY:
        if item.throwable:
            # Cannot throw weapons that are equipped.
            if item.equipable and item.equipable.equipped:
                message = Message(f"Cannot throw equipped weapon {item.name}")
                player_turn_results.append({ResultTypes.MESSAGE: message})
                return
            player_turn_results.extend(item.throwable.throw(game_map, player))
            player_turn_results.extend(item.consumable.consume())
    elif game_state == GameStates.EQUIP_INVENTORY:
        if item.equipable and item.equipable.equipped:
            player_turn_results.extend(item.equipable.remove(player))
        elif item.equipable:
            player_turn_results.extend(item.equipable.equip(player))
    elif game_state == GameStates.DROP_INVENTORY:
        player_turn_results.extend(player.inventory.drop(item))


def player_move_or_attack(move, *,
                          player=None,
                          game_map=None,
                          player_turn_results=None):
    dx, dy = move
    destination_x, destination_y = player.x + dx, player.y + dy
    if game_map.walkable[destination_x, destination_y]:
        blocker = get_blocking_entity_in_position(
            game_map, (destination_x, destination_y))
        # If you attempted to walk into a square occupied by an entity,
        # and that entity is not yourself.
        if blocker and blocker != player:
            attack_results = player.attacker.attack(game_map, blocker)
            player_turn_results.extend(attack_results)
        elif player.attacker.move_callback:
            attack_results = player.attacker.move_callback.execute(
                game_map, player, (destination_x, destination_y))
            player_turn_results.extend(attack_results)
        else:
            player_turn_results.append({
                ResultTypes.END_TURN: True,
                ResultTypes.MOVE: (dx, dy)})


def pickup_entity(game_map, player, player_turn_results):
    for entity in game_map.entities:
        if (entity.pickupable
            and entity.x == player.x and entity.y == player.y):
            pickup_results = player.inventory.pickup(entity)
            player_turn_results.extend(pickup_results)
            break
    else:
        player_turn_results.append({
            ResultTypes.MESSAGE: Message("There is nothing to pick up!")})


def encroach_on_all(encroacher, game_map):
    results = []
    entities = get_all_entities_with_component_in_position(
        (encroacher.x, encroacher.y), game_map, "encroachable")
    if entities:
        for entity in entities:
            results.extend(
                entity.encroachable.encroach(game_map, encroacher))
    return results


def process_damage(game_map, result_data, turn_results):
    target, source, amount, elements = result_data
    if target.defender:
        turn_results.extend(target.defender.transform(
            game_map, source, amount, elements))
    else:
        turn_results.append({ResultTypes.HARM: result_data})


def process_harm(game_map, result_data, turn_results, harmed_queue):
    target, source, amount, elements = result_data
    turn_results.extend(target.harmable.harm(
        game_map, source, amount, elements))
    if target not in harmed_queue:
        harmed_queue.appendleft(target)


def apply_status(entity, player, player_status_manger, enemy_status_manager):
    if entity.status_manager:
        entity.status_manager.remove()
    if entity == player:
        status_manager = player_status_manger()
        status_manager.attach(player)
    else:
        status_manager = enemy_status_manager()
        status_manager.attach(entity)


def entity_equip_armor(entity, armor, turn_results):
    if not hasattr(entity, "harmable"):
        raise AttributeError(
            "Non harmable entities cannot equip Armor")
    if entity.equipment.armor or armor.equipable.equipped:
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} cannot equip {armor.name}",
                COLORS['white'])})
    else:
        entity.equipment.armor = armor
        armor.equipable.equipped = True
        entity.defender.add_damage_transformers(
            armor.equipable.damage_transformers)
        entity.defender.add_damage_callbacks(
            armor.equipable.damage_callbacks)
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} equipped {armor.name}",
                COLORS['white'])})


def entity_equip_weapon(entity, weapon, turn_results):
    if not hasattr(entity, "attacker"):
        raise AttributeError(
            "Non harmable entities cannot equip Weapons")
    if entity.equipment.weapon or weapon.equipable.equipped:
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} cannot equip {weapon.name}",
                COLORS['white'])})
    else:
        entity.equipment.weapon = weapon
        weapon.equipable.equipped = True
        entity.attacker.add_damage_transformers(
            weapon.equipable.damage_transformers)
        entity.attacker.target_callback = weapon.equipable.target_callback
        entity.attacker.move_callback = weapon.equipable.move_callback
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} equipped {weapon.name}",
                COLORS['white'])})


def entity_remove_armor(entity, armor, turn_results):
    if not hasattr(entity, "harmable"):
        raise AttributeError(
            "Non harmable entities cannot un-equip Armor")
    if not entity.equipment.armor or not armor.equipable.equipped:
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} cannot un-equip {armor.name}",
                COLORS['white'])})
    else:
        entity.equipment.armor = None
        armor.equipable.equipped = False
        entity.defender.remove_damage_transformers(
            armor.equipable.damage_transformers)
        entity.defender.remove_damage_callbacks(
            armor.equipable.damage_callbacks)
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} removed {armor.name}",
                COLORS['white'])})


def entity_remove_weapon(entity, weapon, turn_results):
    if not hasattr(entity, "attacker"):
        raise AttributeError(
            "Non harmable entities cannot un-equip Weapons")
    if not entity.equipment.weapon or not weapon.equipable.equipped:
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} cannot un-equip {weapon.name}",
                COLORS['white'])})
    else:
        entity.equipment.weapon = None
        weapon.equipable.equipped = False
        entity.attacker.remove_damage_transformers(
            weapon.equipable.damage_transformers)
        entity.attacker.target_callback = None
        entity.attacker.move_callback = None
        turn_results.append({
            ResultTypes.MESSAGE: Message(
                f"{entity.name} un-equipped {weapon.name}",
                COLORS['white'])})
