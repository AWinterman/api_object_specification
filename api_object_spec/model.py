# TODO: these can probably just be a combination of named tuples and enums.

class Constraint(object):
    repeated = False
    # This is present because some methods will override __init__
    model = None

    def __init__(self, data, model):
        self.model = model
        self._data = data

    @property
    def data(self):
        return self._data


    def __hash__(self):
        return hash(self._data) + hash(self.model)

    def __eq__(self, other):
        return isinstance(self, other) and other.data == self.data and other.model == self.model

    def __iter__(self):
        yield self.data

class Primitive(Constraint):
    pass


class String(Primitive):
    pass


class Number(Primitive):
    pass


class Boolean(Primitive):
    pass


class Collection(Constraint):
    def __init__(self, data, model=None):
        super(Collection, self).__init__(tuple(data), model=model)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


class Array(Collection):
    pass


class Object(Collection):
    pass


class CollectionElement(Constraint):
    # CollectionElements hold a more specific constraint.
    def verbose_text(self, indent=4):
        return 'Container {} for:\n{indent}{}'.format(
            type(self),
            self.data.verbose_text(indent * 2),
            indent=' ' * indent
        )


class ArrayElement(CollectionElement):
    pass


class ObjectElement(CollectionElement):
    pass


class Null(Primitive):
    def __init__(self, model=None):
        super(Null, self).__init__(None, model=model)


class Pair(Constraint):
    def __init__(self, key, value, model):
        # These are wrapped like this so that they have sufficient when yielded out of the iterable of Pair
        self.key = key
        self.value = value

        super(Pair, self).__init__((self.key, self.value), model=model)

class Token(Constraint):
    def __init__(self, name, model=None, repeated=False):
        self.name = name
        self.repeated = repeated

        super(Token, self).__init__((name, repeated), model=model)

class Definitions(Collection):
    # TODO: make the name field not required.
    def __getitem__(self, item):
        return NamedDefinitions([d for d in self.data if d.name == item], name=item, model=self.model)

class NamedDefinitions(Definitions):
    def __init__(self, data, name, model):
        self.name = name
        self.constraint = data
        super(Definitions, self).__init__((tuple(data), name), model=model)

    @property
    def data(self):
        return self.constraint

    def pop(self):
        return NamedDefinitions(self.data, model=self.model)



class Definition(Constraint):
    def __init__(self, name, constraint, model=None):
        self.name = name
        self.constraint = constraint
        self.model = model

        super(Definition, self).__init__((name, constraint), model=model)

    @property
    def data(self):
        return self.constraint

    def __iter__(self):
        yield self.data