import abc
from collections import namedtuple
import random
import configuration


Definition = namedtuple('Definition', ['constraints', 'name'])

# IR nodes and such
class Constraint(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reify(self):
        pass

    # whether the constraint matches the passed json data
    @abc.abstractmethod
    def match(self, data):
        pass

    def __repr__(self):
        return '<{} {}>'.format(type(self), str(self.reify()))


class RefConstraint(Constraint):
    def __init__(self, name):
        self.name = name

    def reify(self):
        # todo: combine this logic with token?
        return "<" + self.name + ">"

    def match(self):
        # TODO: Add actuall method here.
        pass


class UserRefConstraint(RefConstraint):
    def __init__(self, name, possible_values):
        self.name = name
        self.possible_values = possible_values

    def match(self, data):
        return data in self.possible_values

    def reify(self):
        return random.choice(self.possible_values)


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

    def reify(self):
        return {"foo":"bar"}

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

<<<<<<< HEAD
    def match(self, array):
        print isinstance(self.constraint, RepeatedTokenConstraint), self.constraint
        if not isinstance(self.constraint, RepeatedTokenConstraint):
            return self.constraint.match(array[self.index])

        i = self.index

        while i < array.length:
            print i, array[i]
            if not self.constraint.match(array[i]):
                return False

        return True

=======
>>>>>>> e777e700efd65da3c2a17cb99a8d20ae87089a1b
    def reify(self):
        return self.constraint.reify()

    def match(self, array):
        return self.constraint.match(array[self.index])


class ArrayConstraint(Constraint):
    def __init__(self, constraints):
        self.constraints = constraints

    def reify(self):
        output = []
        for element in self.constraints:
            if isinstance(element.constraint, RepeatedTokenConstraint):
                output.extend(element.reify())
            else:
                output.append(element.reify())
        return output

    def match(self, data):
        if not isinstance(data, list):
            return False

        for element in self.constraints:
            print element.reify()
            if not element.match(data):
                return False

        return True

class ArrayRefConstraint(RefConstraint):
    def __init__(self, name):
        RefConstraint.__init__(self, name)

    def reify(self):
        return ["foo", "bar", 1, 2, 3]

    def match(self, data):
        return isinstance(data, list)

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

    def reify(self):
        return "foobar"

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

    def reify(self):
        return 123

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

    def reify(self):
        return random.choice([True, False])

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
        # TODO: make this throw better
        self.definitions = definitions[name]

    def reify(self):
        # todo: do we actually want to make random choices here?
        return random.choice(self.definitions).constraints.reify()

    def match(self, data):

        for definition in self.definitions:
            if definition.constraints.match(data):
                return True
        return False


class RepeatedTokenConstraint(TokenConstraint):
    def __init__(self, name, definitions):
        TokenConstraint.__init__(self, name, definitions)

    def reify(self):
        count = range(0, random.randint(0, configuration.max_generation_count))
        return [super(RepeatedTokenConstraint, self).reify() for _ in count]

    def match(self, data):
        return all(super(RepeatedTokenConstraint, self).match(element) for element in data)


class KeyValueConstraint(Constraint):
    def __init__(self, constraint):
        if not any([
                isinstance(constraint, RepeatedTokenConstraint),
                isinstance(constraint, TokenConstraint),
                isinstance(constraint, PairConstraint),
        ]):
            raise ValueError('"{}" is not a repeated token, a token, or a pair constraint'.format(Constraint))

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
        key = self.key.reify()
        if self.key.match(data):
            # gross
            if self.value.match(data[self.key.reify()]):
                return True
        return False
