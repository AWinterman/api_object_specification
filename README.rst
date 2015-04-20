API Object Specification
========================

.. contents::

Overview
--------

A DSL for writing specifications of JSON APIs, and an accompanying
implementation written in python. This package generates a parser and generator
for APIs defined by a spec file.

Why not just use a CFG?
-----------------------

CFGs are great! 

But JSON APIs often have characteristics that don't match CFGs terribly well.
The DSL actually is a CFG with the following additional characteristics:

- Includes the base JSON types as terminal symbols
- Its JSON object keys are order insensitive: ``{"foo": 1, "bar": 2}`` matches
  ``{"bar": 2, "foo": 1}`` (This is hard to do with a CFG)
- Is whitespace insensitive (where appropriate).
- Knows when to add and when not to add a comma.

Perhaps more importantly, CFGs are not terribly easy to read.

This is awfully JSON specific!
-------------------------------

You're right! I only write JSON APIs these days, but it doesn't seem
unreasonable to extend the specification to support other formats in the
future.


.. _specification-format:

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

If the content type of the api is JSON (configurable), then the following tokens are defined as primitives.

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

        FOO_WRAPPER: {
          "foo": "bar"
          "obj": <object>
        }

        FOO_WRAPPER: {
          "foo": "bar"
          "array": <array>
        }

Repeated Values
***************

``...``
  The equivalent of the Kleane star-- the object must have zero or more
  repetitions of the proceeding token.

::

      STRINGS: [<string>... ]

If there must be at least two strings, then you can say

::

      STRINGS: [<string>, <string>, <string>... ]



Likewise, you can specify any number of keys of a certain type:

::

    FLEXIBLE: {
      <PAIRS>...
    }

    PAIRS: "narcissus": "man"
    PAIRS: "echo": "nymph"
    PAIRS: "zues": "god"

Commas will automatically be added where needed.

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
4. If a regular expression operation rule is used, repeat step (3) until one of the following conditions has been met: 

   - We have exhausted the regular expression operator.
   - The candidate object's entry at the keypath has been consumed.
   - We generated a value a configurable maximum number of times.

Is this fast? Probably not. I haven't written it yet, let alone checked its
performance characteristics. Like most readable pieces of code, it probably
won't be.

To Do
-----
- Configuration documentation
- API documentation
- Write a parser which translates the dsl into a data structure representing expectations about a JSON object.
- Write a generator which constructs objects according to the data structure described above
- Write a parser which is configured with the expectations data structure described above, 
  and takes json objects as input. It should either be a callable or have a method which returns true if an object conforms to
  expectations, and false otherwise.
