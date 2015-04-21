from collections import namedtuple
from parsimonious import NodeVisitor, rule

from enum import Enum


DSL = r"""# A grammar for specifying JSON
# DSL specific
definitions = (definition)*
definition = name "=" element
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
pair = (string ":" pair_value) / token
pair_value = value / one_token
array = "[" elements "]"
elements = (element ("," element)*)?

primitive = (string / number  / true_false_null)
true_false_null = "true" / "false" / "null"

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


class Visitor(NodeVisitor):
    name = None

    def __init__(self, node):
        self.visit(node)

    def generic_visit(self, node, visited_children):
        return node

    def visit_pair(self, node, vc):
        for child in node.children:
            for n in child:
                if not n.expr_name:
                    continue

                print 'child of pair', n.text, n.expr_name


    def visit_name(self, node, vc):
        self.name = node.text


def query_expr_name(node, expr_name, depth_first=True):
    return traverse(node, MatchExprName(expr_name), depth_first=depth_first)


class Model(object):
    def __init__(self, node):
        self.node = node
        self.children = node.children

        if 'node' in dsl or 'children' in dsl or 'text' in dsl:
            raise NameError('Name Error: Please avoid naming rules "node" or "children"')

    @property
    def text(self):
        return self.node.text.strip()

    def __getattr__(self, item):
        return [Model(result) for result in query_expr_name(self.node, item)]


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
    def __init__(self, expr_name):
        self.expr_name = expr_name

    def __call__(self, node):
        matches = node.expr_name == self.expr_name

        return Condition(match=matches, descend=True)


class Type(Enum):
    object = 1
    array = 2
    string = 3
    boolean = 4
    null = 5
    token = 6

Constraint = namedtuple('Constraint', ['type', 'value', 'repeated'])
Definition = namedtuple('Definition', ['constraints', 'name'])


class ConstraintSet(object):
    _constraints = []

    def constrain(self, constraint):
        self._constraints.append(constraint)

    def __repr__(self):
        return "<Definition {name}; constraints: {constraints}>".format(name=self.name, constraints=self._constraints)


class ObjectConstraints(ConstraintSet):
    type = Type.object








