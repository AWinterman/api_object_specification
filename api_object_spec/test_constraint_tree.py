from compile import ApiSpecification, Compiler
import grammar
import model

import unittest


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
            'b': [model.UserRef('b', ['a', 'b', 'c'])],
            'e': [model.UserRef('e', [1, 2, 3])]
        }

        array_constraint = self.c._array(result)

        self.assertEqual(type(array_constraint), model.Array)
        self.assertEqual(len(array_constraint.constraints), 4)

        self.assertTrue(array_constraint.match(['a', 'c', {'c': 'd'}, 1, 2, 3, 1, 2, 3]))

    # def test_object(self):
    #     tokenvalue = self.constraint_definition.model('{"wutever": <mang>, "such key": "value", <token>, <ssss>...}',
    #                                                   rule='object')
    #
    #     result = self.constraint_definition._object(tokenvalue)
    #
    #     self.assertEqual(result.type, grammar.Type.object)
    #     s = {v.type for v in result.value}
    #     self.assertEqual(len(s), 1)
    #     self.assertEqual(s.pop(), grammar.Type.key_value)
    #
    #     self.assertEqual(result.value[0].value,
    #                      grammar.Constraint(type=grammar.Type.repeated_token, value='ssss'))
    #     self.assertEqual(result.value[1].value,
    #                      grammar.Constraint(type=grammar.Type.token, value='token'))
    #     self.assertEqual(result.value[2].value,
    #                      [grammar.Constraint(type=grammar.Type.key, value='such key'),
    #                       grammar.Constraint(type=grammar.Type.string, value='value')])

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
            apathy = {<token>...}

            apathetics = [<apathy>...]

        '''.strip())

