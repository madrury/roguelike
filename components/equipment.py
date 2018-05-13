class Equipment:
    """Holds equipment currently equipped on an entity."""
    def __init__(self):
        self.armor = None
        self.weapon = None

    def equip_armor(self, armor):
        self.armor = armor
