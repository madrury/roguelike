from etc.colors import COLORS
from messages import Message
from game_events import fireblast, waterblast

from etc.enum import (
    ResultTypes, CursorTypes, Animations, EntityTypes, Elements)
from utils.utils import (
    distance_to,
    get_all_entities_with_component_in_position,
    get_n_closest_entities_of_type)
from etc.game_config import (
    HEALTH_POTION_HEAL_AMOUNT,
    MAGIC_MISSILE_BASE_DAMAGE, MAGIC_MISSILE_RANGE, MAGIC_MISSILE_N_TARGETS,
    FIREBLAST_SCROLL_RADIUS, FIREBLAST_SCROLL_BASE_DAMAGE,
    WATERBLAST_SCROLL_RADIUS, WATERBLAST_SCROLL_BASE_DAMAGE)


class NullUsable:
    
    def use(self, game_map, user):
        return []

    def __bool__(self):
        return False


class HealthPotionUsable:
    """A health potion.

    When used on an entity, heals some amount of HP.

    Attributes
    ----------
    name: str
      The name of this item.

    healing: int
      The amount of healing in this potion.
    """
    def __init__(self, healing=HEALTH_POTION_HEAL_AMOUNT):
        self.name = "Healing Potion"
        self.healing = healing

    def use(self, game_map, reciever):
        """Use the health potion on a reciever."""
        results = []
        if reciever.harmable.hp == reciever.harmable.max_hp:
            message = Message(f'{reciever.name} is already at full health.', 
                              COLORS.get('white'))
            results.append({ResultTypes.MESSAGE: message})
        else:
            message = Message(f"{reciever.name}'s wounds start to heal.", 
                              COLORS.get('green'))
            results.append({
                ResultTypes.DAMAGE: (
                    reciever, None, -self.healing, [Elements.HEALING]),
                ResultTypes.MESSAGE: message,
                ResultTypes.ANIMATION: (
                    Animations.HEALTH_POTION, 
                    (reciever.x, reciever.y))})
        return results


class MagicMissileUsable:
    """A Magic Missile spell.

    This targets the closest n entities of a given type, and deals a fixed
    amount of non-elemental elemental damage.

    Attributes
    ----------
    name: str
      The name of this item.

    damage: int
      The amount of damage dealt by the missile.

    spell_range: int
      The maximum distance to an entity able to be targeted.

    n_targets: int
      The number of entities to target.  Each target is damaged by a missile.
    """
    def __init__(self, damage=MAGIC_MISSILE_BASE_DAMAGE,
                       spell_range=MAGIC_MISSILE_RANGE,
                       n_targets=MAGIC_MISSILE_N_TARGETS):
        self.name = "Scroll of Magic Missile"
        self.damage = damage
        self.spell_range = spell_range
        self.n_targets = n_targets

    def use(self, game_map, user, target_type=EntityTypes.MONSTER):
        """Cast the magic missile spell.

        Parameters
        ----------
        user: Entity
          The entity casting the spell.

        entities: list[Entity]
          A list of all entities in the current game state.

        target_type: EntityTypes entry
          The type of target for the spell to seek.
        """
        results = []
        closest_monsters = get_n_closest_entities_of_type(
            (user.x, user.y), game_map, target_type, self.n_targets)
        if closest_monsters:
            for monster in closest_monsters:
                distance = distance_to((user.x, user.y), (monster.x, monster.y))
                if distance <= self.spell_range:
                    text = 'A shining magic missile pierces the {}'.format(
                        monster.name)
                    message = Message(text, COLORS.get('white'))
                    results.append({ResultTypes.DAMAGE: (
                                        monster, None, self.damage, [Elements.NONE]),
                                    ResultTypes.MESSAGE: message})
            animations = [
                (Animations.MAGIC_MISSILE, (user.x, user.y), (monster.x, monster.y))
                for monster in closest_monsters]
            results.append({
                ResultTypes.ANIMATION: (
                    Animations.SIMULTANEOUS, animations)})               
        else:
            message = Message(
                "A shining magic missile streaks into the darkness.",
                COLORS.get('white'))
            results.append({ResultTypes.MESSAGE: message})
        return results


class FireblastUsable:
    """A fireblast spell.

    Fireblast is an area of effect spell centered at the player.  The fireblast spell:

      - Deals non-elemental damage to all harmable entities within a given
        radius (this is the concussion blast).
      - Burns all burnable entities within a given radius.

    Attributes
    ----------
    name: str
      The name of the component.

    damage: int
      Amount of concussion damage.

    radius: int
      The radius of the fireblast.
    """
    def __init__(self, damage=FIREBLAST_SCROLL_BASE_DAMAGE,
                       radius=FIREBLAST_SCROLL_RADIUS):
        self.name = "Scroll of Fireblast"
        self.damage = damage
        self.radius = radius

    def use(self, game_map, user):
        center = (user.x, user.y)
        results = fireblast(game_map, center,
                            radius=self.radius,
                            damage=self.damage,
                            user=user)
        return results


class WaterblastUsable:
    """A fireblast spell.

    Fireblast is an area of effect spell centered at the player.  The fireblast spell:

      - Deals water-elemental damage to all harmable entities within a given
        radius.
      - Spawns water terrain within the given radius of the player.
    """
    def __init__(self, damage=WATERBLAST_SCROLL_BASE_DAMAGE,
                       radius=WATERBLAST_SCROLL_RADIUS):
        self.name = "Scroll of Waterblast"
        self.damage = damage
        self.radius = radius

    def use(self, game_map, user):
        center = (user.x, user.y)
        results = waterblast(game_map, center,
                            radius=self.radius,
                            damage=self.damage,
                            user=user)
        return results


class TorchUsable:
    """A burning torch.

    The torch can only target adjacent tile.  It burns any burnable entites
    residing in the targeted tile.
    """
    def __init__(self):
        self.name = "Torch"

    def use(self, game_map, user):
        callback = TorchCallback(self, game_map, user)
        return [
            {ResultTypes.CURSOR_MODE: (
                user.x, user.y, callback, CursorTypes.ADJACENT)}]


class TorchCallback:

    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        burnable_entities = get_all_entities_with_component_in_position(
            (x, y), self.game_map, "burnable")
        for entity in burnable_entities:
            results.extend(entity.burnable.burn(self.game_map))
        return results
