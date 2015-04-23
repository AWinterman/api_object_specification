import model
from constraint_tree import Tree
from defaults import definitions

result = model.KeyValueConstraint(
    model.PairConstraint(
        model.TokenConstraint('string', definitions=definitions),
        model.StringConstraint('yes')
    )
)
print result.reify()
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
