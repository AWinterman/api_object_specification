from collections import namedtuple
from parsimonious import NodeVisitor, rule

from enum import Enum


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
from parsimonious.grammar import Grammar

Condition = namedtuple("Condition", ["descend", "match"])

dsl = Grammar(DSL)

def query_expr_name(node, expr_name, depth_first=True):
    return traverse(node, MatchExprName(expr_name=expr_name), depth_first=depth_first)


class Model(object):
    def __init__(self, node):
        if 'node' in dsl or 'children' in dsl or 'text' in dsl or 'type' in dsl:
            raise NameError('Name Error: Please avoid naming rules "node" or "children"')

        self.node = node

    def children(self, expr_name=None):
        include = MatchExprName(expr_name=expr_name)

        return [Model(result) for result in self.node.children if include(result).match]

    @property
    def text(self):
        return self.node.text.strip()

    @property
    def type(self):
        return self.node.expr_type

    def __getattr__(self, item):
        return [Model(result) for result in query_expr_name(self.node, item)]

    def __repr__(self):
        return '<grammar.Model: {}>'.format(self.text)


def traverse(node, evaluate, depth_first=True):
    """
    Given a tree, find all the nodes arrived at by descending only those children who match expr_names at a given level.


    :param: evaluate
        A callable returning a :class:`NodeEvaluation` which determines whether we should descend or (inclusive) yield
        the child.
    """
    trees = [node]

    while trees:
        tree = trees.pop(0)

        condition = evaluate(tree)

        if condition.descend:
            for child in tree.children:
                trees.insert(0 if depth_first else trees.length, child)

        if condition.match:
            yield tree


class MatchExprName(object):
    def __init__(self, expr_name=None, descend=True):
        self.expr_name = expr_name
        self.descend = descend

    def __call__(self, node):
        matches = node.expr_name == self.expr_name if self.expr_name is not None else True

        return Condition(match=matches, descend=self.descend)


class DSLType(Enum):
    object = 1
    array = 2
    string = 3
    boolean = 4
    null = 5
    token = 6
    number = 7

Constraint = namedtuple('Constraint', ['type', 'value', 'repeated'])
Definition = namedtuple('Definition', ['constraints', 'name'])

    
def lex_definition_constraints(self, model):
    definitions = []

    for definition in model.definition:
        constraints = []

        if definition.children('object'):
            for pair in definition.pair:
                # The pair has only one child.
                constraints.extend(handle_token(pair))

        definitions.append(Definition(name=definition.name[0]), constraints=constraints)

    print definitions

def handle_array(node):
    # TODO: actually write this bad boy.
    return []

def handle_value(node):
    constraints = []

    for val in node.children('value'):
        # only one of the following calls should result in a non-empty list
        constraints.extend(handle_object(val))
        constraints.extend(handle_array(val))
        constraints.extend(handle_primitive(val))


def handle_object(node):
    for obj in node.children('object'):
        object_constraints = []
        object_constraints.extend(handle_pair(obj))

    constraints = [Constraint(type=DSLType.object, value=object_constraints, repeated=False)]
    constraints.extend(handle_pair(node))

def handle_pair(node):
    constraints = []

    for pair in node.children('pair'):
        token_constraints = handle_token(pair)
        key_value_constraints = handle_key_value(pair)


def handle_key_value(node):
    for kv in node.children('key_value'):
        key = kv.node.children[0]
        value = kv.node.children[2]

        print key.text, value.text

def handle_token(node):
    constraints = []

    for token in node.children('token'):
        if token.repeated_token:
            constraints.append(Constraint(value=token.token_text[0], type=DSLType.token, repeated=True))
        if token.one_token:
            constraints.append(Constraint(value=token.token_text[0], type=DSLType.token, repeated=False))

    return constraints


def handle_primitive(node):
    constraints = []

    for n in node.children('primitive'):
        if n.string:
            type = DSLType.string
        elif n.number:
            type = DSLType.number
        elif n.boolean:
            type = DSLType.boolean
        elif n.null:
            type = DSLType.null

        constraints.append(Constraint(value=n.text, type=type, repeated=False))

    return constraints











