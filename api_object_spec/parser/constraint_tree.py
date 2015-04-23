import model
import grammar
import defaults


class Tree(object):
    def __init__(self, jsl, constraints=defaults.constraints):
        grammar_model = self.grammar_model(jsl)
        self.definitions = {}

        for ref_constraint in constraints:
            self._add_definition(model.Definition(name=ref_constraint.name, constraints=ref_constraint))

        for definition in grammar_model.definition:
            constraint_definition = self._definition(definition)
            self._add_definition(constraint_definition)

    def validate(self, name, data):
        for definition in self.definitions[name]:
            if definition.constraints.match(data):
                return True
        return False

    def generate(self, name):
        for definition in self.definitions[name]:
            return definition.constraints.reify()

    def _add_definition(self, definition):
        if definition.name in self.definitions:
            self.definitions[definition.name].append(definition)
        else:
            self.definitions[definition.name] = [definition]


    @staticmethod
    def grammar_model(text, rule=None):
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

        return model.Definition(name=node.descend('name')[0].text, constraints=constraints)

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

            constraints.append(model.ArrayElementConstraint(el, index))

        return model.ArrayConstraint(constraints)

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

        return model.ObjectConstraint(pairs)


    def _pair(self, pair):
        token = pair.token
        key = pair.pair_key
        value = pair.pair_value

        # using unpacking here, should only get one element, if you have more it will throw.
        if token:
            return model.KeyValueConstraint(self._token(*token))
        elif key and value:
            return model.KeyValueConstraint(model.PairConstraint(self._pair_key(*key), self._pair_value(*value)))
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

        return model.TokenConstraint(name, self.definitions)

    def _repeated_token(self, token):
        name = token.descend('token_text')[0].text

        return model.RepeatedTokenConstraint(name, self.definitions)

    def _primitive(self, n):
        if n.string:
            return self._string(n)
        elif n.number:
            return model.NumberConstraint(float(n.text))
        elif n.boolean:
            tf = {'true': True, 'false': False}[n.text]
            return model.BooleanConstraint(tf)
        elif n.null:
            return model.NullConstraint()
        else:
            raise ValueError('{} is not a primitive'.format(n))

    @staticmethod
    def _string(n):
        return model.StringConstraint(n.text.strip('"'))



#####

sampleJSL = """

wow = "such":"pair"
name = "randy"
hyderabad = {"anynumber": <number>}
things = ["foo", "barf", "dear friends", <string>...]
red = {"subjective":true, "rgb":"1 0 0"}
foo = {"color":<red>, "doge":<wow>, "bar":<hyderabad>, "my name is":<name>, "neat":12.59199, "cool":{"yay":"radical"}}

"""
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