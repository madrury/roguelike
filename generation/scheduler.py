class CompositeScheduler:
    """Represent a schedule for spawning entities on a floor, and implement
    an algebra of schedules with allows for combining schedules probabalistically.

    A spawn schedule is an assignment of a probability distribution over the
    possible spawn groups for some entity type (for example, monsters or
    items). A single group describes how entities will spawin in a single
    room, so this probability distribution describes how groups will spawn in
    a given floor by defining how likely each group is to appear in any given
    room.

    This class is intended to be subclassed by concrete schedulers. These
    will need to define a class attribute `default_group`.
    """
    def __init__(self, group_distribution=None):
        if group_distribution:
            self.group_distribution = group_distribution
        else:
            self.group_distribution = {self.default_group: 1.0}

    def __or__(self, other):
        all_groups = set(self.group_distribution.keys()) | set(other.group_distribution.keys())
        total_probability = sum(
            self.group_distribution.get(group, 0.0) + other.group_distribution.get(group, 0.0)
            for group in all_groups
        )
        merged_groups = {
            group: (
                (self.group_distribution.get(group, 0.0)
                + other.group_distribution.get(group, 0.0)) / total_probability)
            for group in all_groups
        }
        return self.__class__(group_distribution=merged_groups)

    def to_list_of_tuples(self):
        lot = []
        for group, prob in self.group_distribution.items():
            lot.append((prob, group))
        return lot