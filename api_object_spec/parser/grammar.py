from collections import namedtuple, defaultdict
from enum import Enum
from parsimonious.grammar import Grammar

DSL = r"""# A grammar for specifying JSON
# DSL specific
definitions = (definition)*
definition = name "=" (pair / value)
name = space ~"[A-Z_]"i* space
token = repeated_token / one_token
repeated_token = space rpt space
one_token  = space tkn space
tkn = "<" token_text ">"
rpt = "<" token_text ">..."
token_text =  ~"[A-Z_ ]"i*

# JSON
value = space (primitive / object / array) space
element = value / token

object = space "{" (pair ("," pair)*)? "}" space
pair = (pair_key ":" pair_value) / token
pair_key = (one_token / string)
pair_value = value / one_token

array = "[" (element ("," element)*)? "]"

primitive = (string / number  / boolean / null)
boolean = "true" / "false"
null = "null"

string = space "\"" ~"[^\"]"* "\"" space
number = (int frac exp) / (int exp) / (int frac) / int
int = "-"? ((digit1to9 digits) / digit)
frac = "." digits
exp = e digits
digits = digit+
e = "e+" / "e-" / "e" / "E+" / "E-" / "E"

digit1to9 = ~"[1-9]"
digit = ~"[0-9]"
space = ~"\s*"
"""

dsl = Grammar(DSL)

Condition = namedtuple("Condition", ["descend", "match"])


def get_children(item):
    return item.children


def traverse(node, evaluate, depth_first=True, next_generation=get_children):
    trees = [node]

    while trees:
        tree = trees.pop(0)

        condition = evaluate(tree)

        if condition.descend:
            for child in next_generation(tree):
                trees.insert(0 if depth_first else len(trees), child)

        if condition.match:
            yield tree


class Model(object):
    """
    Given a parsed grammar, make a model object for easy querying.

    Exposes a nodes children matching expr_name as getattr(model, expr_name).

    Reserves the following names. You won't be able to look these up if you use them in your grammar:
        - text
        - type
        - descend
    """

    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return (Model(result) for child in self.node.children for result in
                traverse(child, MatchExprBlankDescends(expr_name=None, ignore=['space'])))

    def __getattr__(self, name):
        if name == 'type':
            return self.node.expr_name
        elif name == 'text':
            return self.node.text.strip()
        elif name not in dsl:
            raise AttributeError('Attribute "{}" not found'.format(name))

        # descends through spaces and through unnamed groups. Unnamed matches are usually regex, or expressions of
        # named groups.
        return [Model(result) for child in self.node.children for result in
                traverse(child, MatchExprBlankDescends(expr_name=name, ignore=['space']))]

    def descend(self, item):
        """
        Descend the parsed tree for all expr_name matching items.
        """
        return [Model(result) for result in traverse(self.node, MatchExprName(expr_name=item))]

    def __repr__(self):
        return '<grammar.Model: "{}" with type {}>'.format(self.text, self.type)


class MatchExprName(object):
    def __init__(self, expr_name=None, descend=True):
        self.expr_name = expr_name
        self.descend = descend

    def __call__(self, node):
        matches = node.expr_name == self.expr_name if self.expr_name is not None else True

        return Condition(match=matches, descend=self.descend)


class MatchExprBlankDescends(object):
    def __init__(self, expr_name=None, ignore=()):
        self.expr_name = expr_name
        self.ignore = ignore

    def __call__(self, node):
        descend = not node.expr_name or node.expr_name in self.ignore

        matches = node.expr_name == self.expr_name if self.expr_name is not None else not descend

        return Condition(match=matches, descend=descend)


Constraint = namedtuple('Constraint', ['type', 'value'])
Definition = namedtuple('Definition', ['constraints', 'name'])

class Type(Enum):
    """
    Defines the various types of constraints allowed.
    """
    # Literals
    string = 0
    boolean = 1
    null = 2
    number = 3

    # Tokens
    token = 4
    repeated_token = 5

    # A pair of key/value constraints. Done like this because they are connected (the value constraint
    # needs the key constraint to be meaningful)
    key_value = 10
    key = 11  # Indicates an object/array must have the given key/index
    value = 12  # Indicates the value constraints at a given key/index.

    # The same as the above except for array elements.
    array_element = 13
    index = 14
    element = 15

    # JSON collection types
    object = 6
    array = 7

    @property
    def is_token(self):
        return self in [Type.token, Type.repeated_token]

    @property
    def has_children(self):
        return self in [Type.object, Type.array, Type.array_element, Type.key_value]

    @property
    def is_leaf(self):
        return not self.has_children


class KeyValueConstraint(Constraint):
    type = Type.key_value

    def __new__(cls, key, value):
        print type, value

    def __init__(self, key, value):
        print self


class ConstraintDefinition(Type):
    """
    Instantiates a callable which takes text as input and returns a constraint tree as output.
    """

    def __call__(self, text):
        model = self.model(text)

        definitions = []

        for definition in model.definition:
            definitions.append(self._definition(definition))

        return definitions

    @staticmethod
    def model(text, rule=None):
        if rule is not None:
            model = Model(dsl[rule].parse(text))
        else:
            model = Model(dsl.parse(text))

        return model

    def _definition(self, node):
        kv = node.pair
        val = node.value

        if kv:
            constraints = Constraint(type=Type.key_value, value=self._pair(*kv))
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

            index_constraint = Constraint(type=Type.index, value=index)
            element_constraint = Constraint(type=Type.element, value=el)

            constraints.append(
                Constraint(type=Type.array_element, value=[index_constraint, element_constraint]))

        return Constraint(type=Type.array, value=constraints)

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
        constraints = []

        for pair in obj.pair:
            constraints.append(self._pair(pair))

        return Constraint(type=Type.object, value=constraints)

    def _pair(self, pair):
        token = pair.token
        key = pair.pair_key
        value = pair.pair_value

        # using unpacking here, should only get one element, if you have more it will throw.
        if token:
            return Constraint(type=Type.key_value, value=self._token(*token))
        elif key and value:
            return Constraint(type=Type.key_value, value=[self._pair_key(*key), self._pair_value(*value)])
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

    @staticmethod
    def _one_token(token):
        return Constraint(value=token.descend('token_text')[0].text, type=Type.token)


    @staticmethod
    def _repeated_token(token):
        return Constraint(value=token.descend('token_text')[0].text, type=Type.repeated_token)

    def _primitive(self, n):
        value = n.text

        if n.string:
            return self._string(n)
        elif n.number:
            dsl_type = Type.number
        elif n.boolean:
            dsl_type = Type.boolean
        elif n.null:
            dsl_type = Type.null
        else:
            raise ValueError('"{}" is not a primitive'.format(n))

        return Constraint(value=value, type=dsl_type)

    @staticmethod
    def _string(n):
        dsl_type = Type.string
        value = n.text[1:-1]

        return Constraint(value=value, type=dsl_type)
