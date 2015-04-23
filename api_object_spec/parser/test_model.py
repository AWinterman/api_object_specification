import model
from defaults import definitions

result = model.KeyValueConstraint(
    model.PairConstraint(
        model.TokenConstraint('string', definitions=definitions),
        model.StringConstraint('yes')
    )
)
print result.reify()

print result.match({'wutever': 'yes'})
