from messages import Message
from entity import get_first_blocking_entity_along_path
from etc.colors import COLORS
from etc.enum import EntityTypes, ItemTargeting, ResultTypes, Animations


class HealthPotionComponent:
    """A health component.

    Used on the player themselves, this heals some amount of HP.
    """
    def __init__(self, healing=5):
        self.name = "healing potion"
        self.targeting = ItemTargeting.PLAYER
        self.healing = healing

    def use(self, player):
        results = []
        if player.harmable.hp == player.harmable.max_hp:
            message = Message('You are already at full health.', 
                              COLORS.get('white'))
            results.append({ResultTypes.ITEM_CONSUMED: (False, self.owner), 
                            ResultTypes.MESSAGE: message})
        else:
            message = Message('You wounds start to heal.', 
                              COLORS.get('green'))
            results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                            ResultTypes.HEAL: (player, self.healing),
                            ResultTypes.MESSAGE: message,
                            ResultTypes.ANIMATION: (
                                Animations.HEALTH_POTION, player)})
        return results


class MagicMissileComponent:
    """A Magic Missile spell.

    This targets the closest enemy, and deals an amount of damage.
    """
    def __init__(self, damage=6, spell_range=12):
        self.name = "magic missile"
        self.targeting = ItemTargeting.CLOSEST_MONSTER
        self.damage = damage
        self.spell_range = spell_range

    def use(self, source, entities):
        results = []
        closest_monster = source.get_closest_entity_of_type(
            entities, EntityTypes.MONSTER)
        if (closest_monster and 
            source.distance_to(closest_monster) <= self.spell_range):
            text = 'A shining magic missile pierces the {}'.format(
                closest_monster.name)
            message = Message(text, COLORS.get('white'))
            results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                            ResultTypes.DAMAGE: (closest_monster, self.damage),
                            ResultTypes.MESSAGE: message,
                            ResultTypes.ANIMATION: (
                                Animations.MAGIC_MISSILE,
                                (source.x, source.y),
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
        self.damage = damage

    def use(self, game_map, source, entities):
        callback = ThrowingKnifeCallback(self, game_map, source, entities)
        return [
            {ResultTypes.CURSOR_MODE: (source[0], source[1], callback)}]


class ThrowingKnifeCallback:
    
    def __init__(self, owner, game_map, source, entities):
        self.owner = owner
        self.game_map = game_map
        self.source = source
        self.entities = entities

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_path(
            self.game_map, self.entities, self.source, (x, y))
        if monster:
            text = "The throwing knife pierces the {}'s flesh.".format(
                monster.name)
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (monster, self.owner.damage),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner),
                # TODO: This should pass back the position data for the animation,
                #       not an entity.
                ResultTypes.ANIMATION: (
                    Animations.THROWING_KNIFE, monster)
            })
        else:
            # Todo: Have the knife drop on the ground.
            text = "The throwing knife clatters to the ground"
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.ITEM_CONSUMED: (True, self.owner.owner)
            })
        return results
