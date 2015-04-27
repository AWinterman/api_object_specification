from unittest import TestCase

from api_object_spec import model
from api_object_spec import compile
from api_object_spec import match

class TestMatcher(TestCase):
    """
    These tests are integration tests that check from specification parsing through to validation.
    """

    def setUp(self):
        spec = """
            yes = "yes"
            booltrue = true
            null = null
            number = 1
            yes_collection = [<yes>, 2, <number>]
            yes_collection = ["yesyesyes"]
            repeated_yeses = [<yes>...]
            nested_yes = <yes_collection>
            nested_yes = [<nested_yes>]

            pair = <yes>: "affirmative"
            pair = "affirmative": <yes>

            single_obj = {<pair>}
            repeated_obj = {<pair>...}
        """
        self.spec = compile.ApiSpecification(spec)
        self.match = match.Matcher(self.spec.definitions)



    def test_primitives(self):

        result = [
            self.match(self.spec.definitions['yes'], 'yes'),
            self.match(self.spec.definitions['booltrue'], True),
            self.match(self.spec.definitions['null'], None),
            self.match(self.spec.definitions['number'], 1),
        ]

        for r in result:
            self.assertTrue(r)

        bad_result = [
            self.match(self.spec.definitions['yes'], 'no'),
            self.match(self.spec.definitions['booltrue'], False),
            self.match(self.spec.definitions['null'], {}),
            self.match(self.spec.definitions['number'], 3),
        ]

        for r in bad_result:
            self.assertTrue(not r)

    def test_array(self):
        bad_result = [
            self.match(self.spec.definitions['yes_collection'], 'yes'),
            self.match(self.spec.definitions['yes_collection'], True),
            self.match(self.spec.definitions['yes_collection'], None),
            self.match(self.spec.definitions['yes_collection'], 1),
        ]

        for r in bad_result:
            self.assertFalse(r)

        r = self.match(self.spec.definitions['yes_collection'], ('yes', 2, 1))
        self.assertTrue(r)


        r = self.match(self.spec.definitions['yes_collection'], ('yes',))
        self.assertFalse(r)

    def test_repeated_yes(self):
        r = self.match(self.spec.definitions['repeated_yeses'], ('yes', 'yes',))
        self.assertTrue(r)

    def test_recursively_nested_array(self):
        r = self.match(self.spec.definitions['nested_yes'], ('yesyesyes',))

        self.assertTrue(r)

        r = self.match(self.spec.definitions['nested_yes'], (('yesyesyes',),))
        self.assertTrue(r)

        r = self.match(self.spec.definitions['nested_yes'], ((('yesyesyes',),),))
        self.assertTrue(r)






class TestModelCollection(TestCase):
    def test_iter(self):
        m = model.Collection(['wutever', 'mang'])
        self.assertEqual([a for a in m], ['wutever', 'mang'])


