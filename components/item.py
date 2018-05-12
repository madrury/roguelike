from messages import Message
from entity import get_first_blocking_entity_along_path
from etc.colors import COLORS
from etc.enum import EntityTypes, ItemTargeting, ResultTypes, Animations, Elements


class Item:

    def use(self, game_map, reciever, entities):
        message = Message(f"{self.name} is not usable!", COLORS["white"])
        return [{ResultTypes.MESSAGE: message}]

    def throw(self, game_map, reciever, entities):
        message = Message(f"{self.name} is not throwable!", COLORS["white"])
        return [{ResultTypes.MESSAGE: message}]


class FireblastComponent(Item):
    """A fireblast spell.

    Fireblast is an area of effect spell centered at the player.  The fireblast spell:

      - Deals non-elemental damage to all harmable entities within a given
        radius (this is the concussion blast).
      - Burns all burnable entities within a given radius.

    Attributes
    ----------
    name: str
      The name of the component.

    targeting: ItemTargeting entry.
      The targeting style of this item.  The fireblast spell targets all
      entities within a given radius.

    throwable: bool
      The fireblast scroll cannot be thrown.

    damage: int
      Amount of concussion damage.

    radius: int
      The radius of the fireblast.
    """
    def __init__(self, damage=6, radius=4):
        self.name = "Scroll of Fireblast"
        self.targeting = ItemTargeting.WITHIN_RADIUS
        self.throwable = False
        self.damage = damage
        self.radius = radius

    def use(self, game_map, user, entities):
        results = []
        harmable_within_radius = (
            user.get_all_entities_with_component_within_radius(
                entities, "harmable", self.radius))
        burnable_within_radius = (
            user.get_all_entities_with_component_within_radius(
                entities, "burnable", self.radius))
        for entity in (x for x in harmable_within_radius if x != user):
            text = "The {} is caught in the fireblast!".format(
                entity.name)
            message = Message(text, COLORS.get('white'))
            results.append({ResultTypes.DAMAGE: (
                                entity, self.damage, Elements.NONE),
                            ResultTypes.MESSAGE: message})
        for entity in (x for x in burnable_within_radius if x != user):
            results.extend(entity.burnable.burn(game_map))
        results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                        ResultTypes.ANIMATION: (
                             Animations.FIREBLAST, (user.x, user.y), self.radius)})
        return results


class ThrowingKnifeComponent(Item):
    """A throwing kife.

    The throwing knife does non elemental damage to the first harmable entity
    along a path from the user to a selected target.

    Attributes
    ----------
    name: str
      The name of the component.

    targeting: ItemTargeting entry.
      The targeting style of this item. The throwing knife targets the first
      blocking entity along 

    throwable: bool
      The throwing knife can be thrown (right!).

    damage: int
      Amount of damage.
    """
    def __init__(self, damage=10):
        self.name = "Throwing Knife"
        self.targeting = ItemTargeting.FIRST_ALONG_PATH_TO_CURSOR
        self.throwable = True
        self.damage = damage

    def use(self, game_map, user, entities):
        callback = ThrowingKnifeCallback(self, game_map, user, entities)
        return [
            {ResultTypes.CURSOR_MODE: (user.x, user.y, callback)}]

    def throw(self, game_map, user, entities):
        return self.use(game_map, user, entities)


class ThrowingKnifeCallback:
    """A callback for managing throwing a health poition.
    
    Called after the player enters a cursor selection.
    """
    def __init__(self, owner, game_map, user, entities):
        self.owner = owner
        self.game_map = game_map
        self.user = user
        self.entities = entities

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_path(
            self.game_map, self.entities, (self.user.x, self.user.y), (x, y))
        if monster and monster.harmable:
            text = "The throwing knife pierces the {}'s flesh.".format(
                monster.name)
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (monster, self.owner.damage, Elements.NONE),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner),
                ResultTypes.ANIMATION: (
                    Animations.THROWING_KNIFE,
                    (self.user.x, self.user.y),
                    (monster.x, monster.y))})
        else:
            # Todo: Have the knife drop on the ground.
            text = "The throwing knife clatters to the ground"
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner)
            })
        return results
