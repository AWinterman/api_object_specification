import model
import util
from copy import copy
from enum import Enum

class MatchError(Exception):
    pass


class MatchResult(object):
    @classmethod
    def one(cls, value, constraint=None):
        return MatchResult([value], constraint=constraint)

    def __init__(self, values, operation=all, constraint=None):
        self.values = values
        self.operation = operation
        self.constraint = constraint

    def __nonzero__(self):
        return self.operation(self.values)

class Matcher(object):
    def __init__(self, definitions):
        self.definitions = definitions

        # This requires its own state, so it gets its own class.
        self._match_collection = CollectionMatcher(self)

    def __call__(self, constraint, other):
        if isinstance(constraint, model.Collection):
            return self._match_collection(constraint, object)
        elif isinstance(constraint, model.CollectionElement):
            return self(constraint.constraint, other)
        elif isinstance(constraint, model.Primitive):
            # String, Number, Boolean, Null
            return MatchResult.one(other == constraint.data, constraint=constraint)
        elif isinstance(constraint, model.Token):
            # Token, whether repeated or not.
            return self._match_token(constraint, other)
        raise MatchError('{} does not match a known type'.format(other))

    def match_token(constraint, other):
        for definition in constraint.definitions:
            if definition.match(other):
                return True
        return False


class CollectionMatcher(object):
    def __init__(self, matcher):
        self.result = {}
        self.matcher = matcher
        self.other = {}

    def __call__(self, constraint, other):
        self.other = copy(other)

        result = {}

        for d in self._matches(constraint):
            result.update(d)

    def _matches(self, constraint):
        token_collection_members = [] # {<token>}
        literal_key_pairs = [] # {"any old string": "any old value"
        token_key_pairs = [] # {"<token>": "any old value"}

        for c in constraint:
            if self.is_token(c):
                token_collection_members.append(c.constraint)
            elif self.is_token_key(c):
                token_key_pairs.append(c.constraint)
            elif self.is_literal(c):
                literal_key_pairs.append(c.constraint)
            else:
                raise MatchError("invalid token in key position of a literal")

        literals = self._match_pairs(literal_key_pairs, self.is_literal)
        token_keys = self._match_pairs(token_key_pairs, self.is_token_key)
        tokens = self._match_pairs(token_collection_members, self.is_token)

        return literals, token_keys, tokens

    @staticmethod
    def is_literal(c):
        return isinstance(c.constraint, model.Pair) and isinstance(c.constraint.key, model.String)

    @staticmethod
    def is_token_key(c):
        return isinstance(c.constraint, model.Pair) and isinstance(c.constraint.key, model.Token)

    @staticmethod
    def is_token(c):
        isinstance(c.constraint, model.Token)

    def _match_pairs(self, constraints):
        results = {}

        for k, v in enumerate(self.other):
            results_for_key = []
            for c in constraints:
                pair_results = []

                key_match = self.matcher(c.key, k)

                pair_results.append(key_match)

                if key_match:
                    # Then we can just check if other has the right value at that key
                    candidate_value = self.other[k]

                    value_match = self.matcher(c.value, candidate_value)

                    # Remove this key from other so that we don't validate it twice.
                    del self.other[k]

                    pair_results.append(value_match)

                match = MatchResult(pair_results, operation=all, constraint=c)

                results_for_key.append(match)

                if match:
                    if not c.repeated:
                        # If it's not a repeated constraint, remove it after first match.
                        constraints.remove(c)

                    # no need to continue looping, since we found a match.
                    break

            results[k] = MatchResult(results_for_key, operation=any, constraint=c)

        return results





from unittest import TestCase

import model
import compile

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
            yes_collection = [<yes>]
            repeated_yeses = [<yes>...]
            nested_yes = <yes_collection>
            nested_yes = [nested_yes]

            pair = <yes>: "affirmative"
            pair = "affirmative": <yes>

            single_obj = {<pair>}
            repeated_obj = {<pair>...}
        """
        self.result = compile.c(spec)


    def test_match_collection(self):
        pass



class TestModelCollection(TestCase):
    def test_iter(self):
        m = model.Collection(['wutever', 'mang'])
        self.assertEqual([a for a in m], ['wutever', 'mang'])





