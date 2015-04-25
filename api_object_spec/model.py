import abc
import configuration
import rstr
import random
import logging

logger = logging.getLogger(__name__)



class MatchResult(object):
    def __init__(self, value, other=None, source=None, model=None):
        self.model = model
        self.value = value
        self.other = other
        self.source = source

    def __nonzero__(self):
        try:
            result = any(v for v in self.value)
        except:
            result = bool(self.value)

        logger.debug('self.value is {}, which is "{}"'.format(self.value, result))

        return result

    def __repr__(self):
        return '<MatchResult {value} from {text}>'.format(value=bool(self), text=self.model if self.model else '')

    def trace(self):
        trace = []

        entry = "{} {} against constraint {} of type {}".format(
            "Failed to match" if not self else "Matched",
            self.other,
            str(self.model),
            self.model.type
        )

        print self.source

        try:
            for v in self.value:
                trace.extend(v.trace())
        except TypeError:
            pass

        if self.other is not None:
            trace.append(entry)

        return trace

class Constraint(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reify(self):
        pass

    def match(self, data):
        logger.debug('computing result for {} from {}'.format(data, type(self)))
        return MatchResult(self._match(data), other=data, source=self, model=self.model)

    @abc.abstractmethod
    def _match(self, data):
        pass


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

    def _match(self, other):
        return self.constraint.match(other)


class Object(Constraint):
    def __init__(self, pairs, model=None):
        # pairs are either a token constraint or a key value constraint
        self.key_values = pairs
        self.model = model

    def reify(self):
        output = {}
        for key_value in self.key_values:
            r = key_value.reify()
            if isinstance(key_value.constraint, RepeatedToken):
                if not len(r):
                    continue

                for k, v in r:
                    output[k] = v
            else:
                k, v = r

                output[k] = v
        return output

    def _match(self, data):
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

    def _match(self, data):
        return isinstance(data, dict)


class ArrayElement(ConstraintWrapper):
    def __init__(self, constraint, index, model=None):
        self.constraint = constraint
        self.index = index
        self.model = model

    def _match(self, array):
        if not isinstance(self.constraint, RepeatedToken):
            return self.constraint.match(array[self.index])

        i = self.index

        while i < len(array):
            if not self.constraint.match(array[i]):
                return False
            i += 1

        return True


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

    def _match(self, data):
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

    def _match(self, data):
        return isinstance(data, list)


class String(Constraint):
    def __init__(self, string, model=None):
        self.string = string
        self.model = model

    def reify(self):
        return self.string

    def _match(self, data):
        return self.string == data


class StringRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return rstr.xeger('[\w\s]*')

    def _match(self, data):
        return isinstance(data, str)


class Number(Constraint):
    def __init__(self, number, model=None):
        self.number = number
        self.model = model

    def reify(self):
        return self.number

    def _match(self, data):
        return self.number == data


class NumberRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return 123

    def _match(self, data):
        return isinstance(data, (float, int))


class Boolean(Constraint):
    def __init__(self, boolean, model=None):
        self.boolean = boolean
        self.model = model

    def reify(self):
        return self.boolean

    def _match(self, data):
        return self.boolean.match(data)


class BooleanRef(Ref):
    def __init__(self, name, model=None):
        Ref.__init__(self, name, model=model)

    def reify(self):
        return random.choice([True, False])

    def _match(self, data):
        return isinstance(data, bool)


class Null(Constraint):
    def __init__(self, model=None):
        self.model = model

    def reify(self):
        return None

    def _match(self, data):
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

    def _match(self, data):
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

    def _match(self, data):
        conditions = any(self.key.match(k) and self.value.match(v) for k, v in data.items())

        return conditions
