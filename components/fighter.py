class Fighter:

    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        self.hp -= amount

    def attack(self, target):
        damage = self.power - target.fighter.defense
        if damage > 0:
            target.fighter.take_damage(damage)
            print('{0} atacks {1} for {2} HP.'.format(
                self.owner.name.capitalize(), target.name, damage))
        else:
            print('{0} atacks {1}, but does no damage.'.format(
                self.owner.name.capitalize(), target.name))
