import abc
import logging
import util

logger = logging.getLogger(__name__)


class Constraint(object):
    repeated = False

    # This is present because some methods will override __init__
    data = None

    def __init__(self, data, model=None):
        self.model = model
        self.data = data


class Collection(Constraint):

    def __init__(self, constraints, model=None):
        self.model = model
        self.constraints = constraints

    def __iter__(self):
        return iter(self.constraints)

    def reify(self):
        return self.collect(c.reify for c in self.constraints)


class Primitive(Constraint):
    pass


class String(Primitive):
    pass


class Number(Primitive):
    pass

class Boolean(Primitive):
    pass

class CollectionElement(Constraint):
    # CollectionElements hold a more specific constraint.
    __metaclass__ = abc.ABCMeta

    def __init__(self, constraint, model=None):
        self.constraint = constraint

    def __iter__(self):
        yield self.constraint


class Array(Collection):
    pass


class Object(Collection):
    pass


class ArrayElement(CollectionElement):
    pass


class ObjectElement(CollectionElement):
    pass


class Pair(Constraint):
    def __init__(self, key, value):
        # These are wrapped like this so that they have sufficient when yielded out of the iterable of Pair
        self.key = PairKey(key)
        self.value = PairKey(value)

    def __iter__(self):
        yield (self.key, self.value)


class PairKey(CollectionElement):
    @property
    def data(self):
        return self.constraint.data


class PairValue(CollectionElement):
    pass


class Null(Primitive):
    def __init__(self, model=None):
        super(self, Null).__init__(None, model=model)

class Token(Constraint):
    def __init__(self, name, model=None, repeated=False):
        self.name = name
        self.model = model
        self.repeated = repeated

# Definitions would be the collections here, but since they can neither appear, nor be referenced,
# there's no need for a definitions collection object.
class Definition(Constraint):
    def __init__(self, name, constraint, model=None):
        self.name = name
        self.constraint = constraint
        self.model = model

    def __iter__(self):
        yield self.constraint
