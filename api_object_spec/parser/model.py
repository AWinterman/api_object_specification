import grammar
import abc
from collections import namedtuple
import json


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

    @staticmethod
    def wrap(obj):
        if isinstance(obj, Constraint):
            return obj
        else:
            return {
                list: ArrayConstraint(obj),
                dict: ObjectConstraint(obj),
                str: StringConstraint(obj),
                float: NumberConstraint(obj),
                bool: BooleanConstraint(obj),
                None: NullConstraint()
            }[type(obj)]


class RefConstraint(Constraint):
    def __init__(self, name):
        self.name = name
    def reify(self):
        # todo: combine this logic with token?
        return "<" + self.name + ">"

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

class ConstraintModel(object):
    def __init__(self, jsl):
        grammar_model = self.grammar_model(jsl)
        self.definitions = {}

        for ref_constraint in [ObjectRefConstraint("object"), StringRefConstraint("string"), NumberRefConstraint("number"),
                               BooleanRefConstraint("boolean")]:
            self._add_definition(Definition(name=ref_constraint.name, constraints=ref_constraint))

        for definition in grammar_model.definition:
            constraint_definition = self._definition(definition)
            self._add_definition(constraint_definition)

    def validate(self, name, data):
        for definition in self.definitions[name]:
            if definition.constraints.match(data):
                return True
        return False

    def generate(self, name):
        for definition in self.definitions[name]:
            return definition.constraints.reify()

    def _add_definition(self, definition):
        if definition.name in self.definitions:
            self.definitions[definition.name].append(definition)
        else:
            self.definitions[definition.name] = [definition]


    @staticmethod
    def grammar_model(text, rule=None):
        if rule is not None:
            model = grammar.Model(grammar.dsl[rule].parse(text))
        else:
            model = grammar.Model(grammar.dsl.parse(text))

        return model

    def _definition(self, node):
        kv = node.pair
        val = node.value

        if kv:
            constraints = self._pair(*kv)
        elif val:
            constraints = self._value(*val)
        else:
            raise ValueError("{} is not a valid definition body".format(node))

        return Definition(name=node.descend('name')[0].text, constraints=constraints)

    def _array(self, array):
        constraints = []
        elements = array.element
        # for some reason nodes come out in reverse order, hence:
        elements.reverse()

        for index, element in enumerate(elements):
            value = element.value
            token = element.token

            if value:
                el = self._value(*value)
            elif token:
                el = self._token(*token)
            else:
                raise ValueError('"{}" is an illegal element'.format(element))

            constraints.append(ArrayElementConstraint(el, index))

        return ArrayConstraint(constraints)

    def _value(self, val):
        obj = val.object
        array = val.array
        primitive = val.primitive

        # The following calls use argument unpacking, so that they throw if you somehow have too many elements here.
        if obj:
            return self._object(*obj)

        if array:
            return self._array(*array)

        if primitive:
            return self._primitive(*primitive)

        raise ValueError('"{}" is not a value'.format(val))

    def _object(self, obj):

        pairs = []

        for pair in obj.pair:
            pairs.append(self._pair(pair))

        return ObjectConstraint(pairs)


    def _pair(self, pair):
        token = pair.token
        key = pair.pair_key
        value = pair.pair_value

        # using unpacking here, should only get one element, if you have more it will throw.
        if token:
            return KeyValueConstraint(self._token(*token))
        elif key and value:
            return KeyValueConstraint(PairConstraint(self._pair_key(*key), self._pair_value(*value)))
        else:
            raise ValueError('"{}" is not a pair'.format(pair))

    def _pair_key(self, key):
        token = key.one_token
        string = key.string

        if token:
            return self._one_token(*token)
        elif string:
            return self._string(*string)
        else:
            raise ValueError('node "{}" must either be a string or a single token'.format(key))

    def _pair_value(self, node):
        value = node.value
        token = node.one_token

        if token:
            return self._one_token(*token)
        elif value:
            return self._value(*value)
        else:
            raise ValueError('"{}" must be a JSON value or a single token'.format(value))

    def _token(self, token):
        if token.repeated_token:
            return self._repeated_token(token)
        if token.one_token:
            return self._one_token(token)

        raise ValueError('{} is not a token'.format(token))


    def _one_token(self, token):
        name = token.descend('token_text')[0].text

        return TokenConstraint(name, self.definitions)

    def _repeated_token(self, token):
        name = token.descend('token_text')[0].text

        return RepeatedTokenConstraint(name, self.definitions)

    def _primitive(self, n):
        if n.string:
            return self._string(n)
        elif n.number:
            return NumberConstraint(float(n.text))
        elif n.boolean:
            tf = {'true': True, 'false': False}[n.text]
            return BooleanConstraint(tf)
        elif n.null:
            return NullConstraint()
        else:
            raise ValueError('{} is not a primitive'.format(n))

    @staticmethod
    def _string(n):
        return StringConstraint(n.text.strip('"'))

#####

sampleJSL = """

wow = "such":"pair"
name = "randy"
hyderabad = {"anynumber": <number>}
things = ["foo", "barf", "dear friends"]
red = {"subjective":true, "rgb":"1 0 0"}
foo = {"color":<red>, "doge":<wow>, "bar":<hyderabad>, "my name is":<name>, "neat":12.59199, "cool":{"yay":"radical"}}

"""

model = ConstraintModel(sampleJSL)

print(model.generate("foo"))
print(model.validate("foo", {"color":{"subjective":True, "rgb":"1 0 0"}, "doge":{"such":"pair"}, "bar":{"anynumber":42}, "my name is":"randy", "neat":12.59199, "cool":{"yay":"radical"}}))

print(model.generate('things'))
print model.validate('things', ['food', 'barf', 'dear friends'])
print model.generate('wow')