from collections import namedtuple
from parsimonious.grammar import Grammar
from parsimonious.exceptions import ParseError
from api_object_spec.exceptions import ParsimoniousError

DSL = r"""# A grammar for specifying JSON
# DSL specific
definitions = (definition)*
definition = name "=" (pair / value) space
name = space token_text space
token = repeated_token / one_token
repeated_token = space rpt space
one_token  = space tkn space
tkn = "<" token_text ">"
rpt = "<" token_text ">..."
token_text =  ~"[a-zA-Z0-9_ ]"i*

# JSON
pair = (pair_key ":" pair_value) / token
pair_key = space (one_token / string) space
pair_value = space (value / one_token) space

value = space (primitive / object / array) space
element = value / token

object = space "{" (pair ("," pair)*)? "}" space


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


def parse(spec, rule=None):
    try:
        if rule is not None:
            return Model(dsl[rule].parse(spec))
        else:
            return Model(dsl.parse(spec))
    except ParseError as e:
        raise ParsimoniousError(e)


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

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.node == other.node

    def __hash__(self):
        return hash(self.node) + hash(type(self))

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

    def __str__(self):
        return self.text


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
