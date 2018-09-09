from etc.colors import COLORS
from messages import Message
from game_events import fireblast, waterblast, use_staff

from components.callbacks.usable_callbacks import (
    TorchCallback, FireStaffCallback, IceStaffCallback)

from etc.enum import (
    ResultTypes, CursorTypes, Animations, EntityTypes, Elements)
from utils.utils import (
    l2_distance, bresenham_ray,
    get_n_closest_entities_of_type)
from etc.game_config import (
    HEALTH_POTION_HEAL_AMOUNT, HEALTH_POTION_HP_INCREASE_AMOUNT,
    POWER_POTION_INCREASE_AMOUNT,
    MAGIC_MISSILE_BASE_DAMAGE, MAGIC_MISSILE_RANGE, MAGIC_MISSILE_N_TARGETS,
    FIREBLAST_SCROLL_RADIUS, FIREBLAST_SCROLL_BASE_DAMAGE,
    WATERBLAST_SCROLL_RADIUS, WATERBLAST_SCROLL_BASE_DAMAGE)


class NullUsable:
    """Baseline for items that cannot be used, but that may need a usable
    component.  Does nothing when used.
    """
    def use(self, game_map, user):
        return []

    def __bool__(self):
        return False


class HealthPotionUsable:
    """A health potion.
    
    When used on an entity, heals some amount of HP.
    """
    def __init__(self):
        self.name = "Healing Potion"

    def use(self, game_map, reciever):
        """Use the health potion on a reciever."""
        results = []
        message = Message(f"{reciever.name}'s wounds start to heal.", 
                            COLORS.get('green'))
        results.append({
            ResultTypes.DAMAGE: (
                # Note the minus sign, healing is negative damage.
                reciever, None, -HEALTH_POTION_HEAL_AMOUNT, [Elements.HEALING]),
            ResultTypes.INCREASE_MAX_HP: (
                reciever, HEALTH_POTION_HP_INCREASE_AMOUNT),
            ResultTypes.MESSAGE: message,
            ResultTypes.ANIMATION: (
                Animations.HEALTH_POTION, 
                (reciever.x, reciever.y))})
        return results


class PowerPotionUsable:
    """A power potion.

    When used on an entity it permenantly increases their attack power.
    """
    def __init__(self):
        self.name = "Potion of Power"

    def use(self, game_map, reciever):
        results = []
        message = Message(f"{reciever.name}'s attack power increased.", 
                          COLORS.get('green'))
        results.append({
            ResultTypes.INCREASE_ATTACK_POWER: (
                reciever, POWER_POTION_INCREASE_AMOUNT),
            ResultTypes.MESSAGE: message,
            ResultTypes.ANIMATION: (
                Animations.POWER_POTION, 
                (reciever.x, reciever.y))})
        return results


class SpeedPotionUsable:
    """A speed potion.

    Temporarily doubles an entities speed.
    """
    def __init__(self):
        self.name = "Potion of Speed"

    def use(self, game_map, reciever):
        results = []
        message = Message(f"{reciever.name}'s speed doubled.", 
                          COLORS.get('green'))
        results.append({
            ResultTypes.DOUBLE_SPEED: reciever,
            ResultTypes.MESSAGE: message,
            ResultTypes.ANIMATION: (
                Animations.SPEED_POTION, 
                (reciever.x, reciever.y))})
        return results


class TeleportationPotionUsable:
    """A potion of teleportation.

    Immediately moves the entity to a random open space in the map.
    """
    def __init__(self):
        self.name = "Potion of Teleportation"

    def use(self, game_map, reciever):
        results = []
        message = Message(f"The {reciever.name} vanished.", 
                          COLORS.get('green'))
        results.append({
            ResultTypes.MOVE_TO_RANDOM_POSITION: reciever,
            ResultTypes.MESSAGE: message,
            ResultTypes.ANIMATION: (
                Animations.SPEED_POTION, 
                (reciever.x, reciever.y))})
        return results


class ConfusionPotionUsable:
    """A potion of confusion.

    The effect of this potion depends on if it is used on the player, or an enemy:

      - If used on the player, it hijacks all move actions to move the player
        in a random direction.
      - If used on an enemy, the enemy gets an AI that always moves in a random
        direction.

    Both effects wear off after some amount of time.
    """
    def __init__(self):
        self.name = "Potion of Confusion"

    def use(self, game_map, reciever):
        results = []
        message = Message(f"{reciever.name}'s became confused!",
                          COLORS.get('purple'))
        results.append({
            ResultTypes.CONFUSE: reciever,
            ResultTypes.MESSAGE: message,
            ResultTypes.ANIMATION: (
                Animations.CONFUSION_POTION, 
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
                distance = l2_distance((user.x, user.y), (monster.x, monster.y))
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
        return [{
            ResultTypes.CURSOR_MODE: (
                user.x, user.y, callback, CursorTypes.ADJACENT)}]


class FireStaffUsable:
    """A Staff that shoots fireballs.

    Fireballs travel in a straight line until they meet a blocking object.
    Every burnable object encountered along the path of the fireblall is
    burned, as is the final blocking object encountered.
    """
    def __init__(self):
        self.name = "Fire Staff"

    def use(self, game_map, user):
        return use_staff(self, FireStaffCallback, game_map, user)


class IceStaffUsable:

    def __init__(self):
        self.name = "Ice Staff"

    def use(self, game_map, user):
        return use_staff(self, IceStaffCallback, game_map, user)
