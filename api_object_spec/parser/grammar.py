from collections import namedtuple
from enum import Enum
from parsimonious.grammar import Grammar

DSL = r"""# A grammar for specifying JSON
# DSL specific
definitions = (definition)*
definition = name "=" (key_value / value)
name = space ~"[A-Z_]"i* space
token = repeated_token / one_token
repeated_token = space rpt space
one_token  = space tkn space
tkn = "<" token_text ">"
rpt = "<" token_text ">..."
token_text =  ~"[A-Z_]"i*

# JSON
value = space (primitive / object / array) space
element = value / token

object = space "{" (pair ("," pair)*)? "}" space
pair =  key_value / token
key_value = (string ":" (value / one_token))
array = "[" elements "]"
elements = (element ("," element)*)?

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


def traverse(node, evaluate, depth_first=True):
    trees = [node]

    while trees:
        tree = trees.pop(0)

        condition = evaluate(tree)

        if condition.descend:
            for child in tree.children:
                trees.insert(0 if depth_first else trees.length, child)

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
            raise AttributeError('no such expr_type {}'.format(name))

        # descends through spaces and through unnamed groups. Unnamed matches are usually regex, or expressions of
        # named groups.
        return [Model(result) for child in self.node.children for result in
                traverse(child, MatchExprBlankDescends(expr_name=name, ignore=['space']))]

    def descend(self, item):
        """
        Descend the parsed tree for all expr_name matching items.

        :param item:
        :return:
        """
        return [Model(result) for result in traverse(self.node, MatchExprName(expr_name=item))]

    def __repr__(self):
        return '<grammar.Model: {} with type {}>'.format(self.text, self.type)


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


class ConstraintType(Enum):
    """
    Defines the various types of constraints allowed.
    """
    object = 1
    array = 2
    string = 3
    boolean = 4
    null = 5
    number = 7
    token = 7
    repeated_token = 8
    key_value = 9  # A pair of key/value constraints. Done like this because they are connected (the value constraint
                   #  needs the key constraint to be meaningful)
    key = 10  # Indicates an object/array must have the given key/index
    value = 11  # Indicates the value constraints at a given key/index.


class ConstraintDefinition(object):
    """
    Instantiates a callable which takes text as input and returns a constraint tree as output.
    """

    def __call__(self, text):
        model = self.model(text)

        definitions = []

        for definition in model.definitions:
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
        constraints = []

        for key_value in node.key_value:
            constraints.extend(self._key_value(key_value))

        for value in node.value:
            constraints.extend(self._value(value))

        return Definition(name=node.find('name')[0], constraints=constraints)

    @staticmethod
    def _array(node):
        # TODO: actually write this bad boy.
        return []

    def _value(self, val):
        constraints = []

        for obj in val.object:
            constraints.extend(self._object(obj))

        for array in val.array:
            constraints.extend(self._array(array))

        for primitive in val.primitive:
            constraints.extend(self._primitive(primitive))

        return constraints

    def _object(self, obj):
        constraints = []

        for pair in obj.pair:
            constraints.extend(self._pair(pair))

        return [Constraint(type=ConstraintType.object, value=constraints)]

    def _pair(self, pair):
        constraints = []

        for token in pair.token:
            constraints.extend(self._token(token))

        for kv in pair.key_value:
            constraints.extend(Constraint(type=ConstraintType.key_value, value=self._key_value(kv)))

        return constraints

    def _key_value(self, node):
        constraints = []

        children = list(node)

        key = children[0]
        value = children[1]

        constraints.append(Constraint(type=ConstraintType.key, value=key.text))

        if value.type == 'one_token':
            constraints.append(self._one_token(value))

        if value.type == 'value':
            constraints.append(self._value(value))

        return constraints

    def _token(self, node):
        constraints = []

        for token in node.token:
            if token.repeated_token:
                constraints.extend(self._repeated_token(token))
            if token.one_token:
                constraints.extend(self._one_token(token))

        return constraints

    @staticmethod
    def _one_token(token):
        return [Constraint(value=token.descend('token_text')[0], type=ConstraintType.token)]

    @staticmethod
    def _repeated_token(token):
        return [Constraint(value=token.descend('token_text')[0], type=ConstraintType.repeated_token)]

    @staticmethod
    def _primitive(n):
        constraints = []

        if n.string:
            dsl_type = ConstraintType.string
        elif n.number:
            dsl_type = ConstraintType.number
        elif n.boolean:
            dsl_type = ConstraintType.boolean
        elif n.null:
            dsl_type = ConstraintType.null
        else:
            raise ValueError('{} is not a primitive'.format(n))

        constraints.append(Constraint(value=n.text, type=dsl_type))

        return constraints











