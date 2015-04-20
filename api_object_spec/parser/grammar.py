DSL = r"""# A grammar for specifying JSON

value = space (string / number / object / array / true_false_null) space

object = "{" members "}"
members = (pair ("," pair)*)?
pair = (string ":" value) / (string ":" token) / repeated_token
array = "[" elements "]"
elements = (value ("," value)*)?
true_false_null = "true" / "false" / "null"

string = space "\"" char* "\"" space
token = "<" char* ">"
repeated_token = token "..."
char = ~"[A-Z_]"i  # TODO implement the real thing
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

grammar = Grammar(DSL)

