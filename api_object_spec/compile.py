from api_object_spec import model
from api_object_spec import grammar


class Compiler(object):
    def __call__(self, text, definitions=None):
        if definitions is None:
            definitions = []

        m = grammar.parse(text)

        for definition in m.definition:
            definitions.append(self._definition(definition))

        self.definitions = model.Definitions(definitions, model=m)

        return self.definitions


    def _definition(self, node):
        kv = node.pair
        val = node.value

        if kv:
            constraint = self._pair(*kv)
        elif val:
            constraint = self._value(*val)
        else:
            raise ValueError("{} is not a valid definition body".format(node))

        name = node.descend('name')[0].text

        return model.Definition(name, constraint, model=node)

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

            constraints.append(model.ArrayElement(
                model.Pair(
                    model.Number(index, model=element), el, model=element),
                model=element)
            )

        return model.Array(constraints, model=array)

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

        return model.Object(pairs, model=obj)

    def _pair(self, pair):
        token = pair.token
        key = pair.pair_key
        value = pair.pair_value

        # using unpacking here, should only get one element, if you have more it will throw.
        if token:
            return model.ObjectElement(self._token(*token), model=pair)
        elif key and value:
            return model.ObjectElement(model.Pair(self._pair_key(*key), self._pair_value(*value), model=pair), model=pair)
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

        return model.Token(name, model=token)

    def _repeated_token(self, token):
        name = token.descend('token_text')[0].text

        return model.Token(name, model=token, repeated=True)

    def _primitive(self, n):
        if n.string:
            return self._string(n)
        elif n.number:
            return model.Number(float(n.text), model=n)
        elif n.boolean:
            tf = {'true': True, 'false': False}[n.text]
            return model.Boolean(tf, model=n)
        elif n.null:
            return model.Null(model=n)
        else:
            raise ValueError('{} is not a primitive'.format(n))

    @staticmethod
    def _string(n):
        return model.String(n.text.strip('"'), model=n)

c = Compiler()

class ApiSpecification(object):
    def __init__(self, jsl, definitions=None):
        _definitions = [] #defaults.definitions.copy()

        if definitions:
            _definitions.extend(definitions)

        self.definitions = c(jsl, _definitions)

    def validate(self, name, data):
        results = []
        for definition in self.definitions[name]:
            res = definition.match(data)

            results.append(res)

        return model.MatchResult(results, source=definition.model.name[0], other=data)

    def generate(self, name):
        self.definitions[name].reify()