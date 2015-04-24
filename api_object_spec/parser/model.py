import abc
import random
import configuration

# IR nodes and such
class Constraint(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reify(self):
        pass

    # whether the constraint __eq__es the passed json data
    @abc.abstractmethod
    def __eq__(self, data):
        pass

    def __repr__(self):
        return '<{} {}>'.format(type(self), str(self.reify()))


class Ref(Constraint):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name


class ConstraintWrapper(Constraint):
    def __init__(self, constraint):
        self.constraint = constraint

    def reify(self):
        return self.constraint.reify()

    def __eq__(self, other):
        return self.constraint == other


class UserRef(Ref):
    def __init__(self, name, possible_values):
        self.name = name
        self.possible_values = possible_values

    def __eq__(self, data):
        return data in self.possible_values

    def reify(self):
        return random.choice(self.possible_values)


class Object(Constraint):
    def __init__(self, pairs):
        # pairs are either a token constraint or a key value constraint
        self.key_values = pairs

    def reify(self):
        output = {}
        for key_value in self.key_values:
            if isinstance(key_value.constraint, RepeatedToken):
                for k, v in key_value.constraint.reify():
                    output[k] = v
            else:
                k, v = key_value.reify()

            output[k] = v

        return output

    def __eq__(self, data):
        if not isinstance(data, dict):
            return False
        for key_value in self.key_values:
            if not key_value == data:
                return False
        return True


class ObjectRef(Ref):
    def __init__(self, name):
        Ref.__init__(self, name)

    def reify(self):
        return {"foo": "bar"}

    def __eq__(self, data):
        return isinstance(data, dict)


class Key(Constraint):
    def __init__(self, key):
        self.key = key

    def reify(self):
        return self.key

    def __eq__(self, data):
        return self.key in data


class ArrayElement(ConstraintWrapper):
    def __init__(self, constraint, index):
        self.constraint = constraint
        self.index = index

    def __eq__(self, array):
        if not isinstance(self.constraint, RepeatedToken):
            return self.constraint == (array[self.index])

        i = self.index

        while i < array.length:
            if not self.constraint == (array[i]):
                return False

        return True

    def __eq__(self, array):
        return self.constraint == (array[self.index])


class Array(Constraint):
    def __init__(self, constraints):
        self.constraints = constraints

    def reify(self):
        output = []
        for element in self.constraints:
            if isinstance(element.constraint, RepeatedToken):
                output.extend(element.reify())
            else:
                output.append(element.reify())
        return output

    def __eq__(self, data):
        if not isinstance(data, list):
            return False

        for element in self.constraints:
            if not element == (data):
                return False

        return True


class ArrayRef(Ref):
    def __init__(self, name):
        Ref.__init__(self, name)

    def reify(self):
        return ["foo", "bar", 1, 2, 3]

    def __eq__(self, data):
        return isinstance(data, list)


class String(Constraint):
    def __init__(self, string):
        self.string = string

    def reify(self):
        return self.string

    def __eq__(self, data):
        return self.string == data


class StringRef(Ref):
    def __init__(self, name):
        Ref.__init__(self, name)

    def reify(self):
        return "foobar"

    def __eq__(self, data):
        return isinstance(data, str)


class Number(Constraint):
    def __init__(self, number):
        self.number = number

    def reify(self):
        return self.number

    def __eq__(self, data):
        return self.number == data


class NumberRef(Ref):
    def __init__(self, name):
        Ref.__init__(self, name)

    def reify(self):
        return 123

    def __eq__(self, data):
        return isinstance(data, (float, int))


class Boolean(Constraint):
    def __init__(self, boolean):
        self.boolean = boolean

    def reify(self):
        return self.boolean

    def __eq__(self, data):
        return self.boolean == data


class BooleanRef(Ref):
    def __init__(self, name):
        Ref.__init__(self, name)

    def reify(self):
        return random.choice([True, False])

    def __eq__(self, data):
        return isinstance(data, bool)


class Null(Constraint):
    def reify(self):
        return None

    def __eq__(self, data):
        return data is None


class Token(Constraint):
    def __init__(self, name, definitions):
        self.name = name
        # TODO: make this throw better
        self.definitions = definitions[name]

    def reify(self):
        # todo: do we actually want to make random choices here?
        return random.choice(self.definitions).reify()

    def __eq__(self, data):
        for definition in self.definitions:
            if definition == (data):
                return True
        return False


class RepeatedToken(Token):
    def __init__(self, name, definitions):
        Token.__init__(self, name, definitions)

    def reify(self):
        count = range(0, random.randint(0, configuration.max_generation_count))

        return [super(RepeatedToken, self).reify() for _ in count]


class KeyValue(ConstraintWrapper):
    pass


class Pair():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def reify(self):
        kr = self.key.reify()
        vr = self.value.reify()
        return kr, vr

    def __eq__(self, data):
        conditions = any(self.key == (k) and self.value == (v) for k, v in data.items())

        return conditions
