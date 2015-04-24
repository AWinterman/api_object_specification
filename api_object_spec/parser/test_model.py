import model
from constraint_tree import Tree
from defaults import definitions

result = model.KeyValue(
    model.Pair(
        model.Token('string', definitions=definitions),
        model.String('yes')
    )
)

print result.reify()

print result

assert result.match({'wutever': 'yes'})

t = Tree('''
    token = "boogie": <number>
    token = "wutever": "man"
    token = "yessir": "dressir"
    token = "yessir": <object>

    pair = {<token>...}
''')

print t.generate('pair')

examples = [
    {"yessir": {}, "yessir": "dressir"},
    {'boogie': 1}
]

for e in examples:
    assert t.validate('pair', e)
