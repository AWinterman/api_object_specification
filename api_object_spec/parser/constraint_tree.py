from collections import defaultdict
import model
import grammar
import defaults


class Compiler(object):
    def __call__(self, text, definitions=None):
        self.definitions = defaultdict(list, definitions)

        for definition in self.model(text).definition:
            self._definition(definition)

        return self.definitions

    @staticmethod
    def model(text, rule=None):
        if rule is not None:
            return grammar.Model(grammar.dsl[rule].parse(text))
        else:
            return grammar.Model(grammar.dsl.parse(text))

    def _definition(self, node):
        kv = node.pair
        val = node.value

        if kv:
            constraints = self._pair(*kv)
        elif val:
            constraints = self._value(*val)
        else:
            raise ValueError("{} is not a valid definition body".format(node))

        name = node.descend('name')[0].text

        self.definitions[name].append(constraints)

    def _array(self, array):
        constraints = []
        elements = array.element
        # for some reason nodes come out in reverse order, hence:
        elements.reverse()

        for index, element in enumerate(elements):
            value = element.value
            token = element.token

            if value:
                el = self._value(*value)
            elif token:
                el = self._token(*token)
            else:
                raise ValueError('"{}" is an illegal element'.format(element))

            constraints.append(model.ArrayElement(el, index))

        return model.Array(constraints)

    def _value(self, val):
        obj = val.object
        array = val.array
        primitive = val.primitive

        # The following calls use argument unpacking, so that they throw if you somehow have too many elements here.
        if obj:
            return self._object(*obj)

        if array:
            return self._array(*array)

        if primitive:
            return self._primitive(*primitive)

        raise ValueError('"{}" is not a value'.format(val))

    def _object(self, obj):

        pairs = []

        for pair in obj.pair:
            pairs.append(self._pair(pair))

        return model.Object(pairs)

    def _pair(self, pair):
        token = pair.token
        key = pair.pair_key
        value = pair.pair_value

        # using unpacking here, should only get one element, if you have more it will throw.
        if token:
            return model.KeyValue(self._token(*token))
        elif key and value:
            return model.KeyValue(model.Pair(self._pair_key(*key), self._pair_value(*value)))
        else:
            raise ValueError('"{}" is not a pair'.format(pair))

    def _pair_key(self, key):
        token = key.one_token
        string = key.string

        if token:
            return self._one_token(*token)
        elif string:
            return self._string(*string)
        else:
            raise ValueError('node "{}" must either be a string or a single token'.format(key))

    def _pair_value(self, node):
        value = node.value
        token = node.one_token

        if token:
            return self._one_token(*token)
        elif value:
            return self._value(*value)
        else:
            raise ValueError('"{}" must be a JSON value or a single token'.format(value))

    def _token(self, token):
        if token.repeated_token:
            return self._repeated_token(token)
        if token.one_token:
            return self._one_token(token)

        raise ValueError('{} is not a token'.format(token))

    def _one_token(self, token):
        name = token.descend('token_text')[0].text

        return model.Token(name, self.definitions)

    def _repeated_token(self, token):
        name = token.descend('token_text')[0].text

        return model.RepeatedToken(name, self.definitions)

    def _primitive(self, n):
        if n.string:
            return self._string(n)
        elif n.number:
            return model.Number(float(n.text))
        elif n.boolean:
            tf = {'true': True, 'false': False}[n.text]
            return model.Boolean(tf)
        elif n.null:
            return model.Null()
        else:
            raise ValueError('{} is not a primitive'.format(n))

    @staticmethod
    def _string(n):
        return model.String(n.text.strip('"'))


class Tree(object):
    c = Compiler()

    def __init__(self, jsl, definitions=defaults.definitions):
        self.definitions = self.c(jsl, definitions)

    def validate(self, name, data):
        for definition in self.definitions[name]:
            if definition == data:
                return True
        return False

    def generate(self, name):
        for definition in self.definitions[name]:
            return definition.reify()




#####
#
# sampleJSL = """
#
# wow = "such":"pair"
# name = "randy"
# hyderabad = {"anynumber": <number>}
# things = ["foo", "barf", "dear friends", <string>...]
# red = {"subjective":true, "rgb":"1 0 0"}
# foo = {"color":<red>, "doge":<wow>, "bar":<hyderabad>, "my name is":<name>, "neat":12.59199, "cool":{"yay":"radical"}}
#
# """
#
# model = Tree(sampleJSL)
#
# print(model.generate("foo"))
# print(model.validate("foo",
#                      {"color": {"subjective": True, "rgb": "1 0 0"}, "doge": {"such": "pair"}, "bar": {"anynumber": 42},
#                       "my name is": "randy", "neat": 12.59199, "cool": {"yay": "radical"}}))
#
# print(model.generate('things'))
# print model.validate('things', ['food', 'barf', 'dear friends', 'wutever'])
# print model.generate('wow')
