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
        self.assertEqual(result.type, 'repeated_token')

    def test_object(self):
        tokenvalue = self.constraint_definition.model('{"wutever": <mang>, "such key": "value", <token>, <ssss>...}', rule='object')


        # print tokenvalue
        # print tokenvalue.node
        result = self.constraint_definition._object(tokenvalue)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, grammar.ConstraintType.object)

        s = {v.type for v in result[0].value}
        self.assertEqual(len(s), 1)
        self.assertEqual(s.pop(), grammar.ConstraintType.key_value)

        print result[0].value[1]
        print result[0].value[2]
        print result[0].value[3]

        # print self.constraint_definition._object(simple)
        # print self.constraint_definition._object(token)


    def test_key_value(self):
        plain = self.constraint_definition.model('"so": "it goes"', rule='pair')
        with_token = self.constraint_definition.model('"so": <token>', rule='pair')
        with_object = self.constraint_definition.model('"this": {"object": null}', rule='pair')

        print self.constraint_definition._pair(plain)


    def test_definition(self):
        result = grammar.dsl['definition'].parse('pair = "one": "two"')



    def test_lexer(self):
        result = grammar.dsl['definitions'].parse(
            '''
            apathy = {"asif": "icare", "number": 1}
            apathy = {"deeper": {"nesting": {"of": "obj"}}, "another": "key"}
            apathy = {<token>...}
            token = "god": "zeus"
            token = "nymph": "echo"
            token = "man": <human>
        '''.strip())

        model = grammar.Model(result)

        self.lex_definition_constraints(model)

