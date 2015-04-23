import abc
from collections import namedtuple


Definition = namedtuple('Definition', ['constraints', 'name'])

# IR nodes and such
class Constraint(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reify(self):
        return

    # whether the constraint matches the passed json data
    @abc.abstractmethod
    def match(self, data):
        return


class RefConstraint(Constraint):
    def __init__(self, name):
        self.name = name

    def reify(self):
        # todo: combine this logic with token?
        return "<" + self.name + ">"

    def match(self):
        # TODO: Add actuall method here.
        pass


class ObjectConstraint(Constraint):
    def __init__(self, pairs):
        # pairs are either a token constraint or a key value constraint
        self.key_values = pairs

    def reify(self):
        output = {}
        for key_value in self.key_values:
            k, v = key_value.reify()
            output[k] = v
        return output

    def match(self, data):
        if not isinstance(data, dict):
            return False
        for key_value in self.key_values:
            if not key_value.match(data):
                return False
        return True


class ObjectRefConstraint(RefConstraint):
    def __init__(self, name):
        RefConstraint.__init__(self, name)

    def match(self, data):
        return isinstance(data, dict)


class KeyConstraint(Constraint):
    def __init__(self, key):
        self.key = key

    def reify(self):
        return self.key

    def match(self, data):
        return self.key in data


class ArrayElementConstraint(Constraint):
    def __init__(self, constraint, index):
        self.constraint = constraint
        self.index = index

    def match(self, array):
        return self.constraint.match(array[self.index])

    def reify(self):
        return self.constraint.reify()


class ArrayConstraint(Constraint):
    def __init__(self, constraints):
        self.constraints = constraints

    def reify(self):
        output = []
        for element in self.constraints:
            output = element.reify()
        return output

    def match(self, data):
        if not isinstance(data, list):
            return False

        for element in self.constraints:
            if not element.match(data):
                return False

        return True


class StringConstraint(Constraint):
    def __init__(self, string):
        self.string = string

    def reify(self):
        return self.string

    def match(self, data):
        return self.string == data


class StringRefConstraint(RefConstraint):
    def __init__(self, name):
        RefConstraint.__init__(self, name)

    def match(self, data):
        return isinstance(data, str)


class NumberConstraint(Constraint):
    def __init__(self, number):
        self.number = number

    def reify(self):
        return self.number

    def match(self, data):
        return self.number == data


class NumberRefConstraint(RefConstraint):
    def __init__(self, name):
        RefConstraint.__init__(self, name)

    def match(self, data):
        return isinstance(data, (float, int))


class BooleanConstraint(Constraint):
    def __init__(self, boolean):
        self.boolean = boolean

    def reify(self):
        return self.boolean

    def match(self, data):
        return self.boolean == data


class BooleanRefConstraint(RefConstraint):
    def __init__(self, name):
        RefConstraint.__init__(self, name)

    def match(self, data):
        return isinstance(data, bool)


class NullConstraint(Constraint):
    def reify(self):
        return None

    def match(self, data):
        return data == None


class TokenConstraint(Constraint):
    def __init__(self, name, definitions):
        self.name = name
        self.definitions = definitions[name]

    def reify(self):
        # todo, reify as something more appropriate
        return "<" + self.name + ">"

    def match(self, data):
        # this is the real meat and potatoes
        # look up the definition associated with the token name

        for definition in self.definitions:
            if definition.constraints.match(data):
                return True
        return False


class RepeatedTokenConstraint(Constraint):
    def __init__(self, name):
        self.name = name

    def reify(self):
        # todo, reify as something more appropriate
        return "<" + self.name + ">" + "..."

    def match(self, data):
        # not yet
        return False


class KeyValueConstraint(Constraint):
    def __init__(self, constraint):
        # TODO: validate that the constraint is either a pair or a token or repeated token which maps to a pairs
        self.constraint = constraint

    def reify(self):
        return self.constraint.reify()

    def match(self, data):
        return self.constraint.match(data)


class PairConstraint():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def reify(self):
        kr = self.key.reify()
        vr = self.value.reify()
        return kr, vr

    def match(self, data):
        if self.key.match(data):
            # gross
            if self.value.match(data[self.key.key]):
                return True
        return False
