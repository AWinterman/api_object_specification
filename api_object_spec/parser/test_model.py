import unittest
import re
from api_object_spec.parser import model


class TestTokenReference(unittest.TestCase):
    def test_find(self):
        """Finds a token in the simplest case."""

        result = model.TokenReference.find('some stuff <TOKEN>')
        self.assertEquals(result.next(), 'TOKEN')
        self.assertRaises(StopIteration, result.next)

        result = model.TokenReference.find((
            'some stuff <TOKEN>'
            'some other stuff <OTHER_TOKEN>'
            'not at all a token {<=+?>}'
        ))
        self.assertEquals(result.next(), 'TOKEN')
        self.assertEquals(result.next(), 'OTHER_TOKEN')
        self.assertRaises(StopIteration, result.next)

    def test_id(self):
        ref = model.TokenReference('token')
        self.assertEquals(ref.target, 'json-api-token-definition-token')


class TestExtractDefinitions(unittest.TestCase):
    def setUp(self):
        self.easy_definition = (
            'FOO: {"wutever": "mang"}',
            [('FOO', '{"wutever": "mang"}')],
        )
        self.has_token = (
            'FOO: {"yessir": <YESSIR>}',
            [('FOO', '{"yessir": <YESSIR>}')],
        )

        has_multiple_names_input = '\n'.join([
            'BAR: {"yessir": 0}',
            self.easy_definition[0],
            self.has_token[0],
        ])
        has_multiple_names_output = [
            ('BAR', '{"yessir": 0}'),
            ('FOO', '{"wutever": "mang"}'),
            ('FOO', '{"yessir": <YESSIR>}'),
        ]

        self.has_multiple_names = (has_multiple_names_input, has_multiple_names_output)

    def test_finds_easy_definitions(self):
        results = model.DefinitionList('bar').find_entries(self.easy_definition[0])

        self.assertEqual(results, self.easy_definition[1])

    def test_multiple_definitions(self):
        result = model.DefinitionList('bar').find_entries(self.has_multiple_names[0])

        self.assertEqual(result, self.has_multiple_names[1])






