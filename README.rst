API Object Specification
========================

A DSL for writing specifications of JSON APIs, and an accompanying
implementation written in python. This package generates a parser and generator
for APIs defined by a spec file.

Overview
--------

When you write an API, you should be able to write it in such a way that you
can generate examples and validate instances of API objects. This sphinx
extension solves this problem by defining a JSON specification format which can
be included and displayed in a sphinx document.

Features of the format:

- Replacement rules, like a context free grammar
- Includes the base JSON types as terminal symbols
- Its JSON object keys are order insensitive: ``{"foo": 1, "bar": 2}`` matches
  ``{"bar": 2, "foo": 1}`` (This is hard to do with a CFG)
- Is whitespace insensitive where JSON is whitespace insensitive.

To write a specification, include the following directive in your document:

::

    .. json-spec:: FOO_WRAPPER

        FOO_WRAPPER: {
            "foo": "bar",
            "obj": <OBJECT>
        }

This specifies that a ``FOO_WRAPPER`` is any object with a key "foo" mapping to
"bar", and a key "obj" mapping to any JSON object.

Specification Format 
--------------------

Token Reference
***************

Token references look like ``<NAME>``, where ``NAME`` is any alphanumeric
entry. The ``<`` and ``>`` symbols are configurable.

Each TOKEN reference is replaced by the token definition, if it exists. If no
definition exists, the resulting generator and parser classes will have
corresponding methods which throw ``NotImplemented`` exceptions.

Token Definition
****************

Token definitions look like 

::

  NAME: DEFINITION

Where the definition is a JSON blob containing token and non-token entries.

Name may be defined multiple times. The resulting specification accepts any
definition of NAME.

If the content type of the api is JSON (configurable via a property in your
sphinx conf.py), then the following tokens are defined as primitives.

- object
- array
- value
- string
- number
- boolean

Excepting boolean, which is either ``true`` or ``false``, their values are
defined at json.org.

Optional Fields
***************

At current, optional fields are supported simply by specifying two definitions
for the same token name:  For example:

::

    A ``FOO_WRAPPER`` takes the format 

    .. apiobj:: FOO_WRAPPER

        FOO_WRAPPER: {
          "foo": "bar"
          "obj": <object>
        }

    Alternatively, an array might be passed in:

    .. apiobj:: FOO_WRAPPER

        FOO_WRAPPER: {
          "foo": "bar"
          "array": <array>
        }

Operators
*********

Limited regular expression operations on tokens are supported. 

``*``
  The Kleane star-- the object must have zero or more repetitions of the
  proceeding token.
``+``
  the object must have one or more repetitions of the
  proceeding token.
``{n}``
  Where ``n`` is an integer-- the preceding token must appear exactly ``n`` times.
``{n, m}``
  Where ``n`` and ``m`` are integers-- the preceding token must appear between ``n``
  and ``m`` times. 
  
  If ``n`` is absent, the specification will fail to parse.
  If ``m`` is absent, then objects containing at least ``n`` of the preceding
  token  match the specification.

::

    .. apiobj:: STRINGS

        STRINGS: [<string>*]

If there must be at least two strings, then you can say

::

    .. apiobj:: STRINGS

        STRINGS: [<string>{2,}]



Likewise, you can specify any number of keys of a certain type:

::

    .. apiobj:: FLEXIBLE

    FLEXIBLE: {
      <PAIRS>*
    }

    PAIRS: "narcissus": "man"
    PAIRS: "echo": "nymph"
    PAIRS: "zues": "god"


Implementation
--------------

The JSON parser and generator are implemented according to the following steps:

1. Resolve replacement rules until we have a list of rules which consist of
   only literals or terminal symbols. A terminal symbol is a token which either
   has no definition, or whose definition is in terms of the primitives defined
   above.
2. Construct a list of keypath/terminal symbol pairs for each rule.
3. Check or generate a value for each pair-- that is traverse the candidate
   object according to the given keypath, and ensure that it matches the rule's
   definition. The ``FLEXIBLE`` example above requires special casing-- the key
   can match any of the possibilities defined by the replacement rule.
4. If a Regular Expression operation rule is used, repeat step (3) until one of the following conditions has been met: 
    - We have exhausted the regular expression operator.
    - The candidate object's entry at the keypath has been consumed.
    - We generated a value a configurable maximum number of times.

Future Plans
------------

For now, this only targets JSON APIs. It should be extensible to other
formats, should there be a need.
