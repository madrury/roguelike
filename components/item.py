from messages import Message
from entity import get_first_blocking_entity_along_path
from etc.colors import COLORS
from etc.enum import EntityTypes, ItemTargeting, ResultTypes, Animations


class HealthPotionComponent:
    """A health component.

    When used on an entity, heals some amount of HP.

    Attributes
    ----------
    name: str
      The name of this item.

    targeting: ItemTargeting entry.
      The targeting style of this item.  From the ItemTargeting enum.

    healing: int
      The amount of healing in this potion.
    """
    def __init__(self, healing=5):
        self.name = "healing potion"
        self.targeting = ItemTargeting.PLAYER
        self.throwable = True
        self.healing = healing

    def use(self, reciever):
        """Use the health potion on a reciever.

        Arguments
        ---------
        reciever: Entity
          The reciever of the health potion.
        """
        reciever: Entity
        results = []
        if reciever.harmable.hp == reciever.harmable.max_hp:
            message = Message('You are already at full health.', 
                              COLORS.get('white'))
            results.append({ResultTypes.ITEM_CONSUMED: (False, self.owner), 
                            ResultTypes.MESSAGE: message})
        else:
            message = Message('You wounds start to heal.', 
                              COLORS.get('green'))
            results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                            ResultTypes.HEAL: (reciever, self.healing),
                            ResultTypes.MESSAGE: message,
                            ResultTypes.ANIMATION: (
                                Animations.HEALTH_POTION, 
                                (reciever.x, reciever.y),
                                reciever.char,
                                reciever.color)})
        return results

    def throw(self, game_map, thrower, entities):
        callback = HealthPotionCallback(self, game_map, thrower, entities)
        return [
            {ResultTypes.CURSOR_MODE: (thrower.x, thrower.y, callback)}]


class HealthPotionCallback:

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
            #TODO: Use a queue so these read in the correct order.
            retults.append({ResultTypes.ANIMATION: (
                Animations.HEALTH_POTION,
                (target.x, target.y), target.char, target.color)})
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.HEAL: (target, self.owner.healing),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner)}),
        else:
            text = "The health potion splashes on the ground."
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner)})

            throw_animation = (
                Animations.THROW_POTION, (self.user.x, self.user.y), (x, y))
            spill_animation = (Animations.HEALTH_POTION, (x, y), ' ', None)
            results.append({ResultTypes.ANIMATION: (
                Animations.CONCATINATED, (
                    throw_animation, spill_animation))})

        return results


class MagicMissileComponent:
    """A Magic Missile spell.

    This targets the closest entity fo a given type, and deals a fixed amount
    of damage.

    Attributes
    ----------
    name: str
      The name of this item.

    targeting: ItemTargeting entry.
      The targeting style of this item.  From the ItemTargeting enum.

    damage: int
      The amount of damage dealt by the missile.

    spell_range:
      The maximum distance to an entity able to be targeted.
    """
    def __init__(self, damage=6, spell_range=12):
        self.name = "magic missile"
        self.targeting = ItemTargeting.CLOSEST_MONSTER
        self.throwable = False
        self.damage = damage
        self.spell_range = spell_range

    def use(self, user, entities, target_type=EntityTypes.MONSTER):
        """Cast the magic missile spell.

        Arguments
        ---------
        user: Entity
          The entity casting the spell.

        entities: list[Entity]
          A list of all entities in the current game state.

        target_type: EntityTypes entry
          The type of target for the spell to seek.
        """
        results = []
        closest_monster = user.get_closest_entity_of_type(
            entities, target_type)
        if (closest_monster and 
            user.distance_to(closest_monster) <= self.spell_range):
            text = 'A shining magic missile pierces the {}'.format(
                closest_monster.name)
            message = Message(text, COLORS.get('white'))
            results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                            ResultTypes.DAMAGE: (closest_monster, self.damage),
                            ResultTypes.MESSAGE: message,
                            ResultTypes.ANIMATION: (
                                Animations.MAGIC_MISSILE,
                                (user.x, user.y),
                                (closest_monster.x, closest_monster.y))})
        else:
            message = Message(
                "A shining magic missile streaks into the darkness.",
                COLORS.get('white'))
            results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                            ResultTypes.MESSAGE: message})
        return results


class FireblastComponent:

    def __init__(self, damage=10, radius=4):
        self.name = "fireblast"
        self.targeting = ItemTargeting.WITHIN_RADIUS
        self.throwable = False
        self.damage = damage
        self.radius = radius

    def use(self, user, entities):
        results = []
        monsters_within_radius = user.get_all_entities_of_type_within_radius(
            entities, EntityTypes.MONSTER, self.radius)
        for monster in monsters_within_radius:
            text = "The {} is caught in the fireblast!".format(
                monster.name)
            message = Message(text, COLORS.get('white'))
            results.append({ResultTypes.DAMAGE: (monster, self.damage),
                            ResultTypes.MESSAGE: message})
        results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                        ResultTypes.ANIMATION: (
                             Animations.FIREBLAST, (user.x, user.y), self.radius)})
        return results


class ThrowingKnifeComponent:
    
    def __init__(self, damage=10):
        self.name = "throwing knife"
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
    
    def __init__(self, owner, game_map, user, entities):
        self.owner = owner
        self.game_map = game_map
        self.user = user
        self.entities = entities

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_path(
            self.game_map, self.entities, (self.user.x, self.user.y), (x, y))
        if monster:
            text = "The throwing knife pierces the {}'s flesh.".format(
                monster.name)
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (monster, self.owner.damage),
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
