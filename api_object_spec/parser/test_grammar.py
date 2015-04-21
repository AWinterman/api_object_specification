import grammar

import unittest


class TestGrammar(unittest.TestCase):
    def test_token(self):
        result = grammar.dsl['token'].parse('<WUTEVER>')

        self.assertEqual(result.expr_name, 'token')

        model = grammar.Model(result)


    def test_repeated_token(self):
        result = grammar.dsl['token'].parse('<WUTEVER>...')
        model = grammar.Model(result)


    def test_object(self):
        tokenvalue = grammar.dsl['object'].parse('{"wutever": "<mang>"}')
        simple = grammar.dsl['object'].parse('{"wutever": "mang"}')
        bothtoken = grammar.dsl['object'].parse('{<mang>}')

        grammar.handle_pair(grammar.Model(tokenvalue))
        grammar.handle_pair(grammar.Model(simple))
        grammar.handle_pair(grammar.Model(bothtoken))


    def test_key_value(self):
        plain = grammar.dsl['pair'].parse('"so": "it goes"')
        with_token = grammar.dsl['pair'].parse('"so": <token>')
        with_object = grammar.dsl['pair'].parse('"this": {"object": null}')

        grammar.handle_key_value(grammar.Model(plain))
        grammar.handle_key_value(grammar.Model(with_token))
        grammar.handle_key_value(grammar.Model(with_object))


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

