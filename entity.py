import math
import random

from etc.enum import EntityTypes, RenderOrder, RoutingOptions


class Entity:
    """Represents a game entity, i.e. anything that should be drawn on the map.

    Attributes
    ----------
    x: int
      The x position of the entity on the map.

    y: int
      The y position of the entity on the map.

    char: one character string.
      The symbol used to represent the entity on the map.

    name: str
      The name of the entity.

    entity_type: EntityTypes object
      The type of entity.

    fg_color: (int, int, int) RGB value
      The RGB color to draw the entity on the map.

    bg_color: (int, int, int) RGB value
      The background color to draw the entity tile, if any.

    dark_fg_color: (int, int, int) RGB value
      The RGB color to draw the entity on the map when out of view, if if any.

    dark_bg_color: (int, int, int) RGB value
      The background color to draw the entity tile when out of view, if any.

    seen: bool
      Has the player seen the entity?

    visible_out_of_fov: bool
      Should the entity be draw even when out of the players fov?

    blocks: bool
      Does the entity block movement?

    swims: bool
      Can the entity move through water spaces?

    render_order: int
      In which order shoudl the entity be rendered.  For example, the player
      should be rendered after corpses and items.

    Optional Attributes
    -------------------
    These optional attributes add custom behaviour to entities.

    ai: AI object.
      Contains AI logic for monsters.

    attacker: Attacker object
      Manages entities attack attributes.

    burnable: Burnable object.
      Contains logic for results of attempting to burn the entity.

    status_manager: StatusManager object.
      Manages the status of the entity, i.e. if the entity is condused or frozen.

    commitable: Commitable object.
      Contains logic for commiting and deleting an entity to/from the game.

    dissipatable: Dissipatable object.
      Contains logic for the object spontaneously dissapating.

    encroachable: Encroachable object.
      Contains logic for responding to an entity entering the space.

    equipable: Equipable object.
      Contains logic for equipping the entity onto another entity.

    equipment: Equipment objec.
      Manages what the entity currently has equipped.

    harmable: Harmable object
      Manages entities HP attributes.

    inventory: Inventory object.
      Contains logic for managing an inventory.

    item: Item object
      Contains logic for using as an item.

    movable: Movable object.
      Inteface for moving the entity.

    rechargeable: Rechargeable object.
      Manages the recharging of items like staffs.

    scaldable: Scaldable object.
      Interface for scalding an object.

    shimmer: Shimmer object.
      Contains logic for changing the color of the entity according to certain
      triggers.

    spreadable: Spreadable object.
      Contains logic for an entity to self propagate across the map.

    stats: Stats object.
      Holds various statistics about the entity. For eample, holds a weapon's
      attack power and modifier.

    swimmable: Swimmable object.
      Containins stats and logic for the entity swimming.

    throwable: Trowable object.
      Contains logic for throwing the item.

    usable: Usable object.
      Contains logic for using the item.
    """
    def __init__(self,
                 x, y, char, fg_color, name, *,
                 entity_type=None,
                 render_order=RenderOrder.CORPSE,
                 dark_fg_color=None,
                 bg_color=None,
                 dark_bg_color=None,
                 visible_out_of_fov=False,
                 seen=False,
                 blocks=False,
                 routing_avoid=None,
                 # Optional components.
                 ai=None,
                 attacker=None,
                 burnable=None,
                 status_manager=None,
                 consumable=None,
                 commitable=None,
                 defender=None,
                 dissipatable=None,
                 encroachable=None,
                 equipable=None,
                 equipment=None,
                 floatable=None,
                 freezable=None,
                 harmable=None,
                 illuminatable=None,
                 input_handler=None,
                 inventory=None,
                 item=None,
                 movable=None,
                 rechargeable=None,
                 scaldable=None,
                 shimmer=None,
                 spreadable=None,
                 stats=None,
                 swimmable=None,
                 throwable=None,
                 usable=None):

        self.x = x
        self.y = y
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.dark_fg_color = dark_fg_color
        self.dark_bg_color = dark_bg_color
        self.name = name
        self.entity_type = entity_type
        self.visible_out_of_fov=visible_out_of_fov
        self.seen = seen
        self.blocks = blocks
        self.render_order = render_order

        if routing_avoid:
            self.routing_avoid = routing_avoid
        else:
            self.routing_avoid = []

        self.add_component(ai, "ai")
        self.add_component(attacker, "attacker")
        self.add_component(burnable, "burnable")
        self.add_component(status_manager, "status_manager")
        self.add_component(consumable, "consumable")
        self.add_component(commitable, "commitable")
        self.add_component(defender, "defender")
        self.add_component(dissipatable, "dissipatable")
        self.add_component(encroachable, "encroachable")
        self.add_component(equipable, "equipable")
        self.add_component(equipment, "equipment")
        self.add_component(floatable, "floatable")
        self.add_component(freezable, "freezable")
        self.add_component(harmable, "harmable")
        self.add_component(input_handler, "input_handler")
        self.add_component(illuminatable, "illuminatable")
        self.add_component(inventory, "inventory")
        self.add_component(item, "item")
        self.add_component(movable, "movable")
        self.add_component(rechargeable, "rechargeable")
        self.add_component(scaldable, "scaldable")
        self.add_component(shimmer, "shimmer")
        self.add_component(spreadable, "spreadable")
        self.add_component(stats, "stats")
        self.add_component(swimmable, "swimmable")
        self.add_component(usable, "usable")
        self.add_component(throwable, "throwable")

    @property
    def swims(self):
        return RoutingOptions.AVOID_WATER not in self.routing_avoid

    @property
    def pickupable(self):
        return self.usable or self.throwable or self.equipable

    def add_component(self, component, component_name):
        """Add a component as an attribute of the current object, and set the
        owner of the component to the current object.
        """
        if component:
            component.owner = self
        setattr(self, component_name, component)
