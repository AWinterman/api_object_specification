import json

class Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(Decoder, self).__init__(*args, **kwargs)

        # self.standard_json_parser = self.parse_array
        self.parse_array = self.tuple_parser

        # Using the python scanner since the other one apparently ignores its input.
        self.scan_once = json.scanner.py_make_scanner(self)

    def tuple_parser(self, s_and_end, scan_once):
        values, end = json.decoder.JSONArray(s_and_end, scan_once)
        return tuple(values), end


from unittest import TestCase

class TestDecoder(TestCase):
    def setUp(self):
        self.decoder = Decoder()

    def testDecodesIntoTuple(self):
        print self.decoder.scan_once('[1,2,3]', 0)
        self.assertEqual(self.decoder.decode('[1,2,3]'), (1,2,3,))

