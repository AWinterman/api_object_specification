from unittest import TestCase
from api_object_spec import util

class TestRecursivelyIterate(TestCase):
    def test_non_iterable(self):
        self.assertEqual(util.flatten(4), [4])

    def test_iterable(self):
        self.assertEqual(util.flatten(range(10)), range(10))

    def test_iterates_over_deeply_nested_iterables(self):
        input = [
            [1,2,3]
            [[4],[5],[6]]
            [[[7]]]
        ]

        expected_output = [1,2,3,4,5,6,7]

        self.assertEqual(util.flatten(input), expected_output)