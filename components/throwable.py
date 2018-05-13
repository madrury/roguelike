from etc.colors import COLORS
from messages import Message
from entity import get_first_blocking_entity_along_path
from etc.enum import ResultTypes, Animations, Elements


class NullThrowable:

    def throw(self, game_map, throw, entities):
        return []

    def __bool__(self):
        return False


class HealthPotionThrowable:

    def __init__(self, healing=5):
        self.name = "Healing Potion"
        self.healing = healing

    def throw(self, game_map, thrower, entities):
        """Throw the health potion at a target."""
        callback = HealthPotionCallback(self, game_map, thrower, entities)
        return [
            {ResultTypes.CURSOR_MODE: (thrower.x, thrower.y, callback)}]


class HealthPotionCallback:
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
        target = get_first_blocking_entity_along_path(
            self.game_map, self.entities, (self.user.x, self.user.y), (x, y))
        if target:
            text = "The health potion heals the {}'s wounds".format(
                target.name)
            throw_animation = (
                Animations.THROW_POTION,
                (self.user.x, self.user.y), (target.x, target.y))
            heal_animation = (
                Animations.HEALTH_POTION, (target.x, target.y))
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.HEAL: (target, self.owner.healing),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner),
                ResultTypes.ANIMATION: (
                    Animations.CONCATINATED, (throw_animation, heal_animation))
            }),
        else:
            text = "The health potion splashes on the ground."
            throw_animation = (
                Animations.THROW_POTION, (self.user.x, self.user.y), (x, y))
            spill_animation = (Animations.HEALTH_POTION, (x, y))
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner),
                ResultTypes.ANIMATION: (
                    Animations.CONCATINATED, (throw_animation, spill_animation))
            })
        return results


class ThrowingKnifeThrowable:

    def __init__(self, damage=5):
        self.damage = damage

    def throw(self, game_map, user, entities):
        callback = ThrowingKnifeCallback(self, game_map, user, entities)
        return [
            {ResultTypes.CURSOR_MODE: (user.x, user.y, callback)}]


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
                ResultTypes.DAMAGE: (monster, self.owner.damage, [Elements.NONE]),
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
