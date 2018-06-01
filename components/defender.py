class Defender:
    """Component for entities that can defend against damage.

    Attributes
    ----------
    damage_callbacks: List[DamageFilter]
      A list of transformers to reduce (or increase) incoming damage.  Granted by
      armor or status.

    damage_transformers: List[DamageFilter]
      A list of callbacks to call when a damage event is triggered.  Useful for
      things like counterattacks, status triggers, etc.
    """
    def __init__(self, hp, defense, *,
                 damage_transformers=None,
                 damage_callbacks=None):
        self.damage_transformers = []
        self.damage_callbacks = []
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)
        if damage_callbacks:
            for callback in damage_callbacks:
                self.damage_callbacks.append(callback)

    def transform(self, game_map, source, amount, elements):
        """Apply damage from an element or elements.

        It is not neccesarrly that the entity take all of the damage.  The
        entity may have equipment or resistances that grant them transformers for
        incomping damage.

        Damage can be responded to by providing callbacks in the
        damage_callbacks list.  These are called whenver this method is called.
        """
        results = []
        for transformer in self.damage_transformers:
            results.extend(transformer.transform(
                self.owner, source, amount, elements=elements))
        for callback in self.damage_callbacks:
            results.extend(
                callback.execute(self.owner, source, amount, elements))
        return results

    def add_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.append(transformer)

    def remove_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.remove(transformer)

    def add_damage_callbacks(self, callbacks):
        for callback in callbacks:
            self.damage_callbacks.append(callback)

    def remove_damage_callbacks(self, callbacks):
        for callback in callbacks:
            self.damage_callbacks.remove(callback)
