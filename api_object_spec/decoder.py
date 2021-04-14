import json

class List(tuple):
    def __repr__(self):
        return 'List{}'.format(super(List, self).__repr__())

    def copy(self):
        return List([v for v in self])

class Object(frozenset):
    def __new__(cls, dictionary):
        r = super(Object, cls).__new__(cls, dictionary.items())
        return r

    def __init__(self, dictionary):
        self._items = tuple(dictionary.items())

    def __hash__(self):
        return hash(self._items)

    def __getitem__(self, item):
        r = [v for k, v in self._items if k == item]

        print item, self

        if not r:
            raise KeyError("key {} not in Object".format(item))

        return r[0]

    def __iter__(self):
        return (k for k, v in self._items)

    def keys(self):
        return list(iter(self))

    def has_key(self, key):
        return key in self.keys()

    def items(self):
        return self._items

    def iterkeys(self):
        return (k for k, v in self._items)

    def iteritems(self):
        return (v for k, v in self._items)

    def copy(self):
        return Object(dict(self._items))

    def __contains__(self, item):
        return item in [k for k, v in self._items]

    def __repr__(self):
        return 'Object({})'.format(dict(self._items))


class Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(Decoder, self).__init__(*args, **kwargs)

        # self.standard_json_parser = self.parse_array
        self.parse_array = self.tuple_parser

        # Using the python scanner since the other one apparently ignores its input.
        self.scan_once = json.scanner.py_make_scanner(self)

    def tuple_parser(self, s_and_end, scan_once):
        values, end = json.decoder.JSONArray(s_and_end, scan_once)
        return List(values), end


decode = Decoder(object_hook=Object).decode
