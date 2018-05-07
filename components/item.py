from messages import Message
from entity import get_first_blocking_entity_along_path
from etc.colors import COLORS
from etc.enum import EntityTypes, ItemTargeting, ResultTypes, Animations, Elements


class HealthPotionComponent:
    """A health potion.

    When used on an entity, heals some amount of HP.

    Attributes
    ----------
    name: str
      The name of this item.

    targeting: ItemTargeting entry.
      The targeting style of this item.  The health potion targets the user of
      the potion.

    throwable: bool
      The health potion can be thrown.

    healing: int
      The amount of healing in this potion.
    """
    def __init__(self, healing=5):
        self.name = "healing potion"
        # TODO: Change to ItemTargeting.USER
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
                                (reciever.x, reciever.y))})
        return results

    def throw(self, game_map, thrower, entities):
        """Throw the health potion at a target."""
        callback = HealthPotionCallback(self, game_map, thrower, entities)
        return [
            {ResultTypes.CURSOR_MODE: (thrower.x, thrower.y, callback)}]


class HealthPotionCallback:
    """A callback for managing throwing a health poition."""
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


class MagicMissileComponent:
    """A Magic Missile spell.

    This targets the closest n entities of a given type, and deals a fixed
    amount of non-elemental elemental damage.

    Attributes
    ----------
    name: str
      The name of this item.

    targeting: ItemTargeting entry.
      The targeting style of this item.  Magic missile targets the closest
      entities.

    throwable: bool
      The magic missile scroll cannot be thrown.

    damage: int
      The amount of damage dealt by the missile.

    spell_range: int
      The maximum distance to an entity able to be targeted.

    n_targets: int
      The number of entities to target.  Each target is damaged by a missile.
    """
    def __init__(self, damage=6, spell_range=10, n_targets=3):
        self.name = "magic missile"
        self.targeting = ItemTargeting.CLOSEST_MONSTER
        self.throwable = False
        self.damage = damage
        self.spell_range = spell_range
        self.n_targets = n_targets

    def use(self, user, entities, target_type=EntityTypes.MONSTER):
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
        closest_monsters = user.get_n_closest_entities_of_type(
            entities, target_type, self.n_targets)
        if closest_monsters:
            for monster in (m for m in closest_monsters 
                            if user.distance_to(m) <= self.spell_range):
                text = 'A shining magic missile pierces the {}'.format(
                    monster.name)
                message = Message(text, COLORS.get('white'))
                results.append({ResultTypes.DAMAGE: (
                                   monster, self.damage, Elements.NONE),
                                ResultTypes.MESSAGE: message})
            animations = [
                (Animations.MAGIC_MISSILE, (user.x, user.y), (monster.x, monster.y))
                for monster in closest_monsters]
            results.append({
                ResultTypes.ITEM_CONSUMED: (True, self.owner),
                ResultTypes.ANIMATION: (
                    Animations.SIMULTANEOUS, animations)})               
        else:
            message = Message(
                "A shining magic missile streaks into the darkness.",
                COLORS.get('white'))
            results.append({ResultTypes.ITEM_CONSUMED: (True, self.owner),
                            ResultTypes.MESSAGE: message})
        return results


class FireblastComponent:
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
        self.name = "fireblast"
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
