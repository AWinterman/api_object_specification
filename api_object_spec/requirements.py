class Requirements(object):
    """
    A light wrapper around some sets, encoding the idea that:

    1. We always want to iterate the same set
    2. We want to exhaust the set as constraints are satisfied
    3. We need to know what constraints are unsatisfied
    4. Some constraints should be checked even after they are satisfied.
    """

    def __init__(self, requirements):
        self.requirements = set(requirements)

        if len(requirements) != len(self.requirements):
            raise ValueError('duplicated requirements')

        self.satisfied = set()
        self._check = set(self.requirements)

    @property
    def unsatisfied(self):
        return [r for r in self.requirements if self._unsatisfied(r) ]

    def _unsatisfied(self, r):
        return r not in self.satisfied

    def satisfy(self, r, repeated=False, condition=True):
        if not condition:
            return

        self.satisfied.add(r)

        if repeated:
            return

        self._check.remove(r)

    def __iter__(self):
        return iter([c for c in self._check])

    def __len__(self):
        return len(self.requirements)