from api_object_spec import model
from api_object_spec.compile import ApiSpecification

result = model.KeyValue(
    model.Pair(
        model.Token('string'),
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

    o = {<token>...}
''')

print t.generate('pair')

examples = [
    {"yessir": {}, "yessir": "dressir"},
    {'boogie': 1}
]

bad_examples = [
    {'not a key': 1}
]

for e in examples:
    r = t.validate('o', e)
    assert r

for e in bad_examples:
    r = t.validate('o', e)
    print r.trace(), 'bad result'

    assert not r

t = ApiSpecification('token = {"1": <number>}')
t = ApiSpecification('''
    token = <string>: {
        "1": <number>
    }
''')

