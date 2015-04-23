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

    def test_array(self):
        result = self.constraint_definition.model('["a", <b>, {"c": "d"}, <e>...]', rule="array")

        array_constraint = self.constraint_definition._array(result)

        self.assertEqual(array_constraint.type, grammar.Type.array)
        self.assertEqual(len(array_constraint.value), 4)
        self.assertEqual(array_constraint.value[0].value[0].value, 0)
        self.assertEqual(array_constraint.value[0].value[0].type, grammar.Type.index)
        self.assertEqual(array_constraint.value[0].value[1].value, grammar.Constraint(value='a', type=grammar.Type.string))


    def test_object(self):
        tokenvalue = self.constraint_definition.model('{"wutever": <mang>, "such key": "value", <token>, <ssss>...}',
                                                      rule='object')

        result = self.constraint_definition._object(tokenvalue)

        self.assertEqual(result.type, grammar.Type.object)
        s = {v.type for v in result.value}
        self.assertEqual(len(s), 1)
        self.assertEqual(s.pop(), grammar.Type.key_value)

        self.assertEqual(result.value[0].value,
                         grammar.Constraint(type=grammar.Type.repeated_token, value='ssss'))
        self.assertEqual(result.value[1].value,
                         grammar.Constraint(type=grammar.Type.token, value='token'))
        self.assertEqual(result.value[2].value,
                         [grammar.Constraint(type=grammar.Type.key, value='such key'),
                          grammar.Constraint(type=grammar.Type.string, value='value')])


    def test_key_value(self):
        plain = self.constraint_definition.model('"so": "it goes"', rule='pair')
        with_token = self.constraint_definition.model('"so": <token>', rule='pair')
        with_object = self.constraint_definition.model('"this": {"object": null}', rule='pair')


    def test_definition(self):
        result = grammar.dsl['definition'].parse('pair = "one": "two"')


    def test_call(self):
        result = self.constraint_definition(
            '''
            apathetics = [<apathy>...]
            apathy = {"asif": "icare", "number": 1}
            apathy = {"deeper": {"nesting": {"of": "obj"}}, "another": "key"}
            apathy = {<token>...}
            token = "god": "zeus"
            token = "nymph": "echo"
            token = "man": <human>
        '''.strip())

        type = result[0].constraints[0].type


        print (type.is_token, type.is_leaf, type.has_children, type.name)




