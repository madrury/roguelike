from etc.colors import COLORS
from messages import Message
from etc.enum import (
    ResultTypes, CursorTypes, Animations, EntityTypes, Elements)
from utils.utils import (
    distance_to,
    get_all_entities_with_component_within_radius,
    get_all_entities_with_component_in_position,
    get_n_closest_entities_of_type)


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
    # TODO: Move to config.py
    def __init__(self, healing=20):
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
    def __init__(self, damage=6, spell_range=10, n_targets=3):
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
    def __init__(self, damage=6, radius=4):
        self.name = "Scroll of Fireblast"
        self.damage = damage
        self.radius = radius

    def use(self, game_map, user):
        results = []
        harmable_within_radius = (
            get_all_entities_with_component_within_radius(
                (user.x, user.y), game_map, "harmable", self.radius))
        burnable_within_radius = (
            get_all_entities_with_component_within_radius(
                (user.x, user.y), game_map, "burnable", self.radius))
        for entity in (x for x in harmable_within_radius if x != user):
            text = f"The {entity.name} is caught in the fireblast!"
            message = Message(text, COLORS.get('white'))
            results.append({ResultTypes.DAMAGE: (
                                entity, None, self.damage, [Elements.NONE]),
                            ResultTypes.MESSAGE: message})
        for entity in (x for x in burnable_within_radius if x != user):
            results.extend(entity.burnable.burn(game_map))
        results.append({
            ResultTypes.ANIMATION: (
                Animations.FIREBLAST, (user.x, user.y), self.radius)})
        return results


class TorchUsable:
    """A burning torch.

    The torch can only target adjacent tile.  It burns any burnable entites
    residing in the targeted tile.
    """
    def __init__(self, damage=2):
        self.name = "Torch"
        self.damage = damage

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
