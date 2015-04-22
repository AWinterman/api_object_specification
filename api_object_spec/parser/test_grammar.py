import grammar

import unittest


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.constraint_definition = grammar.ConstraintDefinition()

    def test_token(self):
        result = self.constraint_definition.model('<WUTEVER>', rule="token")
        self.assertEqual(result.type, 'token')

    def test_repeated_token(self):
        result = grammar.dsl['token'].parse('<WUTEVER>...')
        self.assertEqual(result.expr_name, 'token')

    def test_object(self):
        tokenvalue = self.constraint_definition.model('{"wutever": <mang>, "such key": "value", <token>, <ssss>...}',
                                                      rule='object')

        result = self.constraint_definition._object(tokenvalue)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, grammar.ConstraintType.object)
        s = {v.type for v in result[0].value}
        self.assertEqual(len(s), 1)
        self.assertEqual(s.pop(), grammar.ConstraintType.key_value)

        self.assertEqual(result[0].value[0].value[0],
                         grammar.Constraint(type=grammar.ConstraintType.repeated_token, value='ssss'))
        self.assertEqual(result[0].value[1].value[0],
                         grammar.Constraint(type=grammar.ConstraintType.token, value='token'))
        self.assertEqual(result[0].value[2].value,
                         [grammar.Constraint(type=grammar.ConstraintType.key, value='such key'),
                          grammar.Constraint(type=grammar.ConstraintType.string, value='value')])


    def test_key_value(self):
        plain = self.constraint_definition.model('"so": "it goes"', rule='pair')
        with_token = self.constraint_definition.model('"so": <token>', rule='pair')
        with_object = self.constraint_definition.model('"this": {"object": null}', rule='pair')


    def test_definition(self):
        result = grammar.dsl['definition'].parse('pair = "one": "two"')


    def test_call(self):
        result = self.constraint_definition(
            '''
            apathy = {"asif": "icare", "number": 1}
            apathy = {"deeper": {"nesting": {"of": "obj"}}, "another": "key"}
            apathy = {<token>...}
            token = "god": "zeus"
            token = "nymph": "echo"
            token = "man": <human>
        '''.strip())

        print result
