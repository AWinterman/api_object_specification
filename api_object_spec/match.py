from collections import Mapping, Sequence, Counter
from api_object_spec import model
from api_object_spec.requirements import Requirements
from copy import copy

class MatchError(Exception):
    pass


class MatchResult(object):
    @classmethod
    def one(cls, value, constraint, other, comment = ''):
        return MatchResult([value], constraint=constraint, other=other, comment=comment)

    @classmethod
    def true(cls, constraint, other, comment):
        return MatchResult([True], constraint, other, comment=comment)

    def __init__(self, values, constraint, other, operation=all, comment=''):
        self.operation = operation
        self.constraint = constraint
        self.other = other
        self.comment = comment
        self.values = values

    def append(self, element):
        self.values.append(element)

    def trace(self, indent=2):
        indent_str = ' ' * indent
        item = '{indent}- {status}: candidate `{other}` {verb}{comment}\n{indent}{constraint}'.format(
            status='SUCCESS' if bool(self) else 'FAILURE',
            other=self.other,
            verb=' succeeded' if bool(self) else 'failed',
            comment=self.comment and ' condition "{}"'.format(self.comment),
            constraint=' against constraint: `{}`'.format(self._format_model_text(self.constraint.model.text, indent_str) if self.constraint else ''),
            indent=indent_str,

        )

        items = [item]

        next_generation = [v.trace(indent=indent+2) for v in self.values if isinstance(v, MatchResult)]

        if next_generation:
            items.append('  {}Needed {} child condition to match:'.format(indent_str, self.operation.__name__))

        items.extend(next_generation)

        return '\n'.join(items)

    def _format_model_text(self, text, indent):
        return '\n' + (indent + '    ') + '\n{}'.format(indent + '    ').join([t.strip() for t in text.split('\n')])

    def __len__(self):
        return len(self.values)

    def __nonzero__(self):
        return self.operation(self.values)

class Matcher(object):
    def __init__(self, definitions):
        self.definitions = definitions

        # This requires its own state, so it gets its own class.
        self._match_collection = CollectionMatcher(self)
        self.token_lookup = Counter()


    def __call__(self, constraint, other):
        if isinstance(constraint, model.Definitions):
            if hasattr(constraint, 'name'):
                comment = "token `{}` appears in definition list".format(constraint.name)
            else:
                comment = "is in specification".format(other)


            return MatchResult(
                [self(d, other) for d in constraint],
                operation=any,
                constraint=constraint,
                other=other,
                comment=comment
            )
        if isinstance(constraint, model.Pair):
            raise NotImplementedError("haven't implemented object pair definitions yet")

        if isinstance(constraint, model.Collection):
            return self._match_collection(constraint, other)

        if isinstance(constraint, model.CollectionElement):
            return self(constraint.data, other)

        if isinstance(constraint, model.Primitive):
            # String, Number, Boolean, Null
            return MatchResult.one(other == constraint.data, constraint=constraint, other=other)

        if isinstance(constraint, model.Token):
            self.token_lookup[constraint.name] += 1
            m = self(self.definitions[constraint.name], other)

            return m
        if isinstance(constraint, model.Definition):
            return self(constraint.data, other)

        raise MatchError('{} of type {} does not match a known type, (matching {})'.format(constraint, type(constraint), other))

    def match_token(constraint, other):
        for definition in constraint.definitions:
            if definition.match(other):
                return True
        return False


class CollectionMatcher(object):
    def __init__(self, matcher):
        self.result = {}
        self.matcher = matcher

    def __call__(self, constraint, other):
        if not (isinstance(other, dict) or isinstance(other, tuple)):
            return MatchResult.one(False, other=other, constraint=constraint)

        self.other = copy(other)
        self.constraint = constraint

        result = {}
        remaining = []

        for d, r in self._matches(constraint):
            result.update(d)
            remaining.extend(r)

        def not_any(x):
            return not x

        m = MatchResult(
            result.values(),
            operation=all,
            constraint=constraint,
            other=other,
            comment='every key fulfills a constraint'
        )

        unused = MatchResult(
            remaining,
            operation=not_any,
            constraint=constraint,
            other=other,
            comment='every constraint is fulfilled'
        )

        return MatchResult([m, unused], constraint=constraint, operation=all, other=other)

    def _matches(self, constraint):
        token_collection_members = [] # {<token>}
        literal_key_pairs = [] # {"any old string": "any old value"
        token_key_pairs = [] # {"<token>": "any old value"}

        for c in constraint:
            if self.is_token(c):
                token_collection_members.append(c.data)
            elif self.is_token_key(c):
                token_key_pairs.append(c.data)
            elif self.is_literal(c):
                literal_key_pairs.append(c.data)
            else:
                raise MatchError("invalid value in collection a literal. \n Constraint:\n {}".format(c.verbose_text(indent=4)))

        key_requirements = Requirements(set(enumerate(self.other)))

        literals = self._match_pairs(
            key_requirements=key_requirements,
            constraint_requirements=Requirements(literal_key_pairs)
        )

        token_keys = self._match_pairs(
            key_requirements=key_requirements,
            constraint_requirements=Requirements(token_key_pairs)
       )

        tokens = self._match_pairs(
            key_requirements=key_requirements,
            constraint_requirements=Requirements(token_collection_members)
        )

        return literals, token_keys, tokens

    @staticmethod
    def is_literal(c):
        return isinstance(c.data, model.Pair) and any([
            isinstance(c.data.key, model.String),
            isinstance(c.data.key, model.Number),
        ])

    @staticmethod
    def is_token_key(c):
        return isinstance(c.data, model.Pair) and isinstance(c.data.key, model.Token)

    @staticmethod
    def is_token(c):
        return isinstance(c.data, model.Token) or all([
            isinstance(c.data, model.Pair),
            isinstance(c.data.key, model.Number),
            isinstance(c.data.value, model.Token),
        ])

    def _match_pairs(self, key_requirements, constraint_requirements):
        results = {}

        if not key_requirements:
            return results, []

        for k, v in key_requirements:
            if (k, v) in key_requirements.satisfied:
                continue

            results[k] = MatchResult(
                values=[],
                operation=any,
                comment="key value constraint",
                constraint=self.constraint, other=(k, v)
            )

            for c in constraint_requirements:
                key_match = self.matcher(c.key, k) \

                is_repeated_token_in_array = (
                    # it's a repeated token in an array, and we don't care about the key.
                    isinstance(c.value, model.Token) and c.value.repeated and isinstance(c.key, model.Number)
                )

                if is_repeated_token_in_array:
                    key_match = MatchResult.true(constraint=c, other=k, comment="key for repeated value")

                results[k].append(key_match)

                if key_match:
                    # Then we can just check if other has the right value at that key
                    value_match = self.matcher(c.value, v)

                    results[k].append(value_match)

                constraint_requirements.satisfy(c, repeated=c.value.repeated, condition=key_match and value_match)
                key_requirements.satisfy((k, v), condition=key_match and value_match)

        return results, constraint_requirements.unsatisfied



