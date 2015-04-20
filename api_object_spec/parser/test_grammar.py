from grammar import grammar

import unittest


class TestGrammar(unittest.TestCase):
    def test_token(self):
        result = grammar['token'].parse('<WUTEVER>')

        self.assertEqual(result.expr_name, 'token')
        self.assertEqual(result.children[1], 'WUTEVER')

    def test_repeated_token(self):
        result = grammar['repeated_token'].parse('<WUTEVER>...')

        self.assertEqual(result.expr_name, 'repeated_token')
        print result.children

    def test_pair(self):
        pass
