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
    pair = {<token>...}
''')

print t.generate('pair')
