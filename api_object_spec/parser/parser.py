import parsimonious

my_grammar = parsimonious.Grammar("""
    object = "{}" / "{" members "}"
    members = pair / pair "," members
    pair = string ":" value
    array = "[]" / "[" elements "]"
    elements = value / value "," elements
    value = string / number / object  / "true" / "false" / "null" / object / array
    string = ~r"[A-Z 0-9]*"i
    number = ~r"[0-9]*"
    """)

print my_grammar