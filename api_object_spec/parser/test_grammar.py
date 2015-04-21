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


    def test_pair(self):
        tokenvalue = grammar.dsl['object'].parse('{"wutever": "<mang>"}')
        simple = grammar.dsl['object'].parse('{"wutever": "mang"}')
        bothtoken = grammar.dsl['object'].parse('{<mang>}')

    def test_definition(self):
        result = grammar.dsl['definitions'].parse(
            '''
            apathy = {"asif": "icare", "number": 1}
            apathy = {"deeper": {"nesting": {"of": "obj"}}, "another": "key"}
            apathy = {<token>...}
        '''.strip())

        model = grammar.Model(result)

        definitions = []

        for definition in model.definition:
            definition_constraint = grammar.ConstraintSet()
            definitions.append(grammar.Definition(name=definition.name[0].text, constraints=definition_constraint))

            if definition.object:
                object_constraints = grammar.ObjectConstraints()

                definition_constraint.constrain(object_constraints)

                for pair in definition.pair:
                    for c in pair.children[0].children:
                        if not c.expr_name:
                            continue

                        if c.expr_name == 'repeated_token':
                            token_name = grammar.query_expr_name(c, 'token_text').next()
                            object_constraints.constrain(pair=token_name, type=grammar.Type.token, repeated=True)

                        if c.expr_name == 'pair_value':





            print result



