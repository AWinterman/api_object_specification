import model
from compile import ApiSpecification
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

t = ApiSpecification('''
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

t = ApiSpecification('token = {"1": <number>}')
t = ApiSpecification('''
    token = <string>: {
        "1": <number>
    }
''')

