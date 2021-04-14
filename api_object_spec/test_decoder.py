from api_object_spec.decoder import decode, List, Object

from unittest import TestCase

class TestDecoder(TestCase):
    def setUp(self):
        self.decode = decode

    def testDecodesIntoTuple(self):
        self.assertEqual(self.decode('[1,2,3]'), (1,2,3,))

    def testDecodesIntoObjects(self):
        print
        self.assertEqual(self.decode('{"l": [1,2,3]}'), Object({"l": (1,2,3,)}))


class TestJSONCollections(TestCase):
    def TestList(self):
        l = List([1,2,3,3,4])

        self.assertIsInstance(l, List)
        self.assertEqual(tuple(l), (1,2,3,3,4))

        threw = False
        try:
            s = set()
            s.add(l)
        except Exception as e:
            threw = e
        finally:
            self.assertFalse(threw)

    def TestObject(self):
        o = Object({'a': 1, '_ wutever i want': 2})
        self.assertIsInstance(o, Object, '{} is not an instance of {}'.format(o, Object))

        self.assertEqual(dict(o), {'a': 1, '_ wutever i want': 2})
