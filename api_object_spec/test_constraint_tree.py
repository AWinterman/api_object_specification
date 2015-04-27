from api_object_spec.compile import ApiSpecification, Compiler
import grammar
import model

import random

import unittest


class UserRef(model.Ref):
    def __init__(self, name, possible_values, model=None):
        self.name = name
        self.possible_values = possible_values
        self.model = model


    def _match(self, data):
        return data in self.possible_values

    def reify(self):
        return random.choice(self.possible_values)


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.c = Compiler()

    def test_token(self):
        result = self.c.model('<WUTEVER>', rule="token")
        self.assertEqual(result.type, 'token')

    def test_repeated_token(self):
        result = grammar.dsl['token'].parse('<WUTEVER>...')
        self.assertEqual(result.expr_name, 'token')

    def test_array(self):
        result = self.c.model('["a", <b>, {"c": "d"}, <e>...]', rule="array")
        self.c.definitions = {
            'b': [UserRef('b', ['a', 'b', 'c'])],
            'e': [UserRef('e', [1, 2, 3])]
        }

        array_constraint = self.c._array(result)

        print array_constraint.reify()

        self.assertEqual(type(array_constraint), model.Array)
        self.assertEqual(len(array_constraint.constraints), 4)

        self.assertTrue(array_constraint.match(['a', 'c', {'c': 'd'}, 1, 2, 3, 1, 2, 3]))

    def test_object(self):
        tokenvalue = self.c.model('{"wutever": <mang>, "such key": "value", <token>: "sup", <ssss>...}',
                                                      rule='object')

        self.c.definitions = {
            'mang': [UserRef('mang', ['a', 'b', 'c'])],
            'token': [UserRef('token', [1, 2, 3])],
            'ssss': [UserRef('sss', [('a', 'b'), ("c", " d")])]
        }

        result = self.c._object(tokenvalue)

        print result.reify()

    def test_key_value(self):
        plain = self.c.model('"so": "it goes"', rule='pair')
        with_token = self.c.model('"so": <token>', rule='pair')
        with_object = self.c.model('"this": {"object": null}', rule='pair')
        token_first = self.c.model('<token>: true', rule='pair')

    def test_definition(self):
        result = ApiSpecification('pair = "one": "two"')

        self.assertEqual(result.generate('pair'), ('one', 'two'))


    def test_call(self):
        t = ApiSpecification(
            '''
            human = "roger"
            human = "steve"
            human = "orange"

            animal_name = "dog"

            token = "god": "zeus"
            token = "nymph": "echo"
            token = "man": <human>
            token = <animal_name>: "animal"

            apathy = {"asif": "icare", "number": 1}
            apathy = {"deeper": {"nesting": {"of": "obj"}}, "another": "key"}
            apathy = { <token>...}

            apathetics = [<apathy>...]

        '''.strip())

        r = t.validate('apathy', {})

        print 'trace:'
        print '\n'.join(str(t) for t in r.trace())