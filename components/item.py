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
