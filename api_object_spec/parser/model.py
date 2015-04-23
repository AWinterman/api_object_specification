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

class KeyValueConstraint(Constraint):
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def reify(self):
        return (self.key.reify(), self.value.reify())
    def match(self, data):
        if self.key.match(data):
            # gross
            if self.value.match(data[self.key.key]):
                return True
        return False

class KeyConstraint(Constraint):
    def __init__(self, key):
        self.key = key
    def reify(self):
        return self.key
    def match(self, data):
        return self.key in data

#  broken until arrays are real
class ArrayConstraint(Constraint):
    def __init__(self, elements):
        self.elements = []
        for element in elements:
            self.elements.append(Constraint.wrap(element))

    def reify(self):
        output = []
        for element in self.elements:
            output = element.reify()
        return output

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
        return false

class ConstraintModel(object):
    """
    Instantiates a callable which takes text as input and returns a constraint tree as output.
    """

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

        for key_value in node.key_value:
            constraints = self._key_value(key_value)

        for value in node.value:
            constraints = self._value(value)

        return Definition(name=node.descend('name')[0].text, constraints=constraints)

    def _array(node):
        # TODO: actually write this bad boy.
        return []

    def _value(self, val):

        for obj in val.object:
            constraints = self._object(obj)

        for array in val.array:
            constraints = self._array(array)

        for primitive in val.primitive:
            constraints = self._primitive(primitive)

        return constraints

    def _object(self, obj):

        pairs = []

        for pair in obj.pair:
            pairs.append(self._pair(pair))

        return ObjectConstraint(pairs)

    def _pair(self, pair):

        # not sure how to handle this one yet?
        for token in pair.token:
            constraints = self._token(token)

        for kv in pair.key_value:
            constraints = self._key_value(kv)

        return constraints

    def _key_value(self, node):

        children = list(node)

        key = children[0]
        value = children[1]

        return KeyValueConstraint(self._key(key), self._kvalue(value))

    def _key(self, key):
        return KeyConstraint(key.text[1:-1])

    def _kvalue(self, value):
        if value.type == 'one_token':
            return self._one_token(value)
        if value.type == 'value':
            return self._value(value)

    def _token(self, token):
        if token.repeated_token:
            return self._repeated_token(token)
        if token.one_token:
            return self._one_token(token)

    def _one_token(self, token):
        name = token.descend('token_text')[0].text
        return TokenConstraint(name, self.definitions)

    def _repeated_token(self, token):
        name = token.descend('token_text')[0].text
        return RepeatedTokenConstraint(name)

    def _primitive(self, n):
        constraints = []

        value = n.text

        if n.string:
            return StringConstraint(n.text.strip('"'))
        elif n.number:
            return NumberConstraint(float(n.text))
        elif n.boolean:
            tf = {'true': True, 'false': False}[n.text]
            return BooleanConstraint(tf)
        elif n.null:
            return NullConstraint()
        else:
            raise ValueError('{} is not a primitive'.format(n))

#####

sampleJSL = """

wow = "such":"pair"
name = "randy"
hyderabad = {"anynumber": <number>}
red = {"subjective":true, "rgb":"1 0 0"}
foo = {"color":<red>, "doge":<wow>, "bar":<hyderabad>, "my name is":<name>, "neat":12.59199, "cool":{"yay":"radical"}}

"""

model = ConstraintModel(sampleJSL)

print(model.generate("foo"))
print(model.validate("foo", {"color":{"subjective":True, "rgb":"1 0 0"}, "doge":{"such":"pair"}, "bar":{"anynumber":42}, "my name is":"randy", "neat":12.59199, "cool":{"yay":"radical"}}))
