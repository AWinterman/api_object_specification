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

object = space "{" members "}" space
members = (pair ("," pair)*)
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


class ConstraintType(Enum):
    """
    Defines the various types of constraints allowed.
    """
    object = 1
    array = 2
    string = 3
    boolean = 4
    null = 5
    token = 6
    number = 7
    key = 8


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
        return (Model(child) for child in self.node.children)

    def __getattr__(self, name):
        if name == 'type':
            return self.node.expr_name
        elif name == 'text':
            return self.node.text.strip()

        include = MatchExprName(expr_name=name)

        return [Model(result) for result in self.node.children if include(result).match]

    def descend(self, item):
        """
        Descend the parsed tree for all expr_name matching items.

        :param item:
        :return:
        """
        return [Model(result) for result in traverse(self.node, MatchExprName(expr_name=item))]

    def __repr__(self):
        return '<grammar.Model: {}>'.format(self.text)


class MatchExprName(object):
    def __init__(self, expr_name=None, descend=True):
        self.expr_name = expr_name
        self.descend = descend

    def __call__(self, node):
        matches = node.expr_name == self.expr_name if self.expr_name is not None else True

        return Condition(match=matches, descend=self.descend)


class ConstraintDefinition(object):
    """
    Instantiates a callable which takes text as input and returns a constraint tree as output.
    """
    Constraint = namedtuple('Constraint', ['type', 'value', 'repeated'])
    Definition = namedtuple('Definition', ['constraints', 'name'])

    def __call__(self, text):
        model = self.model(text)

        definitions = []

        for definition in model.definitions:
            definitions.append(self._definition(definition))

        return definitions

    def model(self, text, rule=None):
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

        return self.Definition(name=node.find('name')[0], constraints=constraints)

    @staticmethod
    def _array(node):
        # TODO: actually write this bad boy.
        return []

    def _value(self, val):
        constraints = []

        # only one of the following calls should result in a non-empty list
        constraints.extend(self._object(val))
        constraints.extend(self._array(val))
        constraints.extend(self._primitive(val))

        return constraints

    def _object(self, obj):
        constraints = []

        for pair in obj.pair:
            object_constraints = self._pair(pair)
            constraints.append(self.Constraint(type=ConstraintType.object, value=object_constraints, repeated=False))

        return constraints

    def _pair(self, pair):
        constraints = []

        for token in pair.token:
            constraints.extend(self._token(token))

        for kv in pair.key_value:
            constraints.extend(self._key_value(kv))

        return constraints

    def _key_value(self, node):
        constraints = []

        children = list(node)

        key = children[0]
        value = children[2]

        constraints.append(self.Constraint(type=ConstraintType.key, value=key, repeated=False))
        constraints.extend(self._value(value))
        constraints.extend(self._token(value))

        return constraints

    def _token(self, node):
        constraints = []

        for token in node.token:
            if token.repeated_token:
                constraints.append(self.Constraint(value=token.token_text[0], type=ConstraintType.token, repeated=True))
            if token.one_token:
                constraints.append(self.Constraint(value=token.token_text[0], type=ConstraintType.token, repeated=False))

        return constraints

    @staticmethod
    def _primitive(self, node):
        constraints = []

        for n in node.children('primitive'):
            if n.string:
                dsl_type = ConstraintType.string
            elif n.number:
                dsl_type = ConstraintType.number
            elif n.boolean:
                dsl_type = ConstraintType.boolean
            elif n.null:
                dsl_type = ConstraintType.null

            constraints.append(self.Constraint(value=n.text, type=dsl_type, repeated=False))

        return constraints











