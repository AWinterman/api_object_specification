
from collections import defaultdict
import collections
import re
import json

json.dump

TOKEN_REGEX = re.compile('<(\w+)>')

class ValueConstraints(object):
    """
    An object representing the constraints upon the JSON objects in the api.
    """

    def __init__(self, text):
        self.text = text

    def parse(self):
        paths = []

        for char in self.text:
            if(char === '{')



class TokenReferences(object):
    """
    :param: text
        The text from which to extract token references.
    """

    _token_regex =


    def __init__(self, text):
        self.text = text

    def open_brace(self):


    def parse(self):
        for char in self.text:










class TokenDefinition(object):
    """
    Encapsulates knowledge about a rule for generating or validating an api component.

    Each API component looks like:

    .. sourcecode:: rst

        .. json-spec:: foo

            FOO: {
                "foo": "bar"
                "obj": <OBJECT>
            }
    """
    #TODO should be an iterator that returns string-token-string etc. for expansion
    #TODO needs to have a name property extracted from text
    #TODO need to define how to look up other tokens, and use their definitions in current expansion.

    def __init__(self, name="", definition=""):
        self._definition = definition
        self._name = name

    @property
    def name(self):
        return self._name

    def __iter__(self):
        pass

    @property
    def references(self):
        (match.group(1) for match in TokenReference.find(self.rule))


class DefinitionList(object):
    """
        Rules appear in a collection, which together define the API specification. Each RuleList is identified by it's api_name field.
    """
    terminals = []
    rules = defaultdict(list)

    name_regex = re.compile("^(\w+?): ", re.M)

    def __init__(self, api_name):
        self.api_name = api_name

    def add_definition(self, rule):
        """Add a new rule to the list"""
        self.rules[rule.name].append(rule)

    def find_terminals(self):
        """
        Given the existing set of rules, compute the terminal symbols assumed by the grammar
        """

        defined_tokens = set(self.rules.keys())
        appearing_tokens = {t for rule in self.rules for t in rule.references}

        return list(appearing_tokens - defined_tokens)

    def find_token_definitions(self, text):
        text = text.strip()
        matches = collections.deque()
        matches.extend(self.name_regex.finditer(text))

        pairs = []

        if not matches:
            return pairs

        match = matches.popleft()
        start = match.start()

        if start != 0:
            raise ValueError(
                'Text has illegal leading characters. Should only lead with whitespace characters when defining '
                'a token'
            )

        name = match.group(1)

        while matches:
            last_match = match
            match = matches.popleft()

            definition = text[last_match.end():match.start()]

            pairs.append((name, definition.strip()))

            name = match.group(1)

        pairs.append((name, text[match.end():].strip()))

        return pairs


