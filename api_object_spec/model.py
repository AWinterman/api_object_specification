import abc
import random
import configuration

class ConstraintError(Exception):
    pass


class Constraint(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reify(self):
        pass

    @abc.abstractmethod
    def match(self, data):
        pass

    def __repr__(self):
        return '<{} definition: \'{}\'>'.format(type(self), self.model.text)


class Ref(Constraint):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, model=None):
        self.name = name
        self.model = model


class ConstraintWrapper(Constraint):
    def __init__(self, constraint, model=None):
        self.constraint = constraint
        self.model = model

    def reify(self):
        return self.constraint.reify()

    def match(self, other):
        return self.constraint.match(other)


class UserRef(Ref):
    def __init__(self, name, possible_values, model=None):
        self.name = name
        self.possible_values = possible_values
        self.model = model


    def match(self, data):
        return data in self.possible_values

    def reify(self):
        return random.choice(self.possible_values)


class Object(Constraint):
    def __init__(self, pairs, model=None):
        # pairs are either a token constraint or a key value constraint
        self.key_values = pairs
        self.model = model


    def reify(self):
        output = {}
        for key_value in self.key_values:
            if isinstance(key_value.constraint, RepeatedToken):
                r = key_value.reify()
                if not r.length:
                    continue
                for k, v in r:
                        output[k] = v
                else:
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


class ObjectRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return {"foo": "bar"}

    def match(self, data):
        return isinstance(data, dict)


class Key(Constraint):
    def __init__(self, key, model=None):
        self.key = key
        self.model = model


    def reify(self):
        return self.key

    def match(self, data):
        return self.key in data


class ArrayElement(ConstraintWrapper):
    def __init__(self, constraint, index, model=None):
        self.constraint = constraint
        self.index = index
        self.model = model

    def match(self, array):
        if not isinstance(self.constraint, RepeatedToken):
            return self.constraint.match(array[self.index])

        i = self.index

        while i < array.length:
            if not self.constraint.match(array[i]):
                return False

        return True

    def match(self, array):
        return self.constraint.match(array[self.index])


class Array(Constraint):
    def __init__(self, constraints, model=None):
        self.constraints = constraints
        self.model = model

    def reify(self):
        output = []
        for element in self.constraints:
            if isinstance(element.constraint, RepeatedToken):
                output.extend(element.reify())
            else:
                output.append(element.reify())
        return output

    def match(self, data):
        if not isinstance(data, list):
            return False

        for element in self.constraints:
            if not element.match(data):
                return False

        return True


class ArrayRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return ["foo", "bar", 1, 2, 3]

    def match(self, data):
        return isinstance(data, list)


class String(Constraint):
    def __init__(self, string, model=None):
        self.string = string
        self.model = model

    def reify(self):
        return self.string

    def match(self, data):
        return self.string == data


class StringRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return "foobar"

    def match(self, data):
        return isinstance(data, str)


class Number(Constraint):
    def __init__(self, number, model=None):
        self.number = number
        self.model = model

    def reify(self):
        return self.number

    def match(self, data):
        return self.number == data


class NumberRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return 123

    def match(self, data):
        return isinstance(data, (float, int))


class Boolean(Constraint):
    def __init__(self, boolean, model=None):
        self.boolean = boolean
        self.model = model

    def reify(self):
        return self.boolean

    def match(self, data):
        return self.boolean.match(data)


class BooleanRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return random.choice([True, False])

    def match(self, data):
        return isinstance(data, bool)


class Null(Constraint):
    def __init__(self, model=None):
        self.model = model

    def reify(self):
        return None

    def match(self, data):
        return data is None


class Token(Constraint):
    def __init__(self, name, definitions, model=None):
        self.name = name
        # TODO: make this throw better
        self.definitions = definitions[name]
        self.model = model

    def reify(self):
        # todo: do we actually want to make random choices here?
        return random.choice(self.definitions).reify()

    def match(self, data):
        for definition in self.definitions:
            if definition.match(data):
                return True
        return False


class RepeatedToken(Token):
    def __init__(self, name, definitions, model=None):
        Token.__init__(self, name, definitions, model=model)

    def reify(self):
        count = range(0, random.randint(0, configuration.max_generation_count))

        return [super(RepeatedToken, self).reify() for _ in count]


class KeyValue(ConstraintWrapper):
    pass


class Pair(Constraint):
    def __init__(self, key, value, model=None):
        self.key = key
        self.value = value
        self.model = model

    def reify(self):
        kr = self.key.reify()
        vr = self.value.reify()

        return kr, vr

    def match(self, data):
        conditions = any(self.key.match(k) and self.value.match(v) for k, v in data.items())

        return conditions