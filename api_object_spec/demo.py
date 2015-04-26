"""
A Presentation on api_object_specification

            Andrew Winterman, Marc Sciglimpaglia

"""

presentation = """

            ==========================
             API Object Specification
            ==========================

   Specifying JSON objects in a simple, human readable format...


    ... And generating parsers/generators from the specification


http://eng-docs.prod.urbanairship.com/docs/api-v3/en/latest/#api-endpoints

- This is pretty good

- Specification can be complex.

For example: API V3: notification.ios.alert

         "alert" - Override the alert value provided at the top level,
          if any. MAY BE A JSON STRING OR AN OBJECT WHICH CONFORMS
          TO APPLE'S SPEC (SEE TABLE 3-2 IN THE APNS DOCS).


              API Implementer's Contract:
              ---------------------------

- Consume the full specification
- Produce valid payloads

- Docs lay out the contract

- There should be a way to verify implementations match
  the docs with computers.
Goal:
     - Write a DSL for specifying JSON objects.
     - Keep it easy to read, easy to write.
     - Keep the rules simple.
     - Compile the DSL into an API generator for
       fuzzing, and a validator

"""

api_v3 = """

atom = {"tag": <string>}
atom = {"segment": <uuid>}

operator = "and"
operator = "or"

selectors = <operator>: [<atom>...]

audience = "all"
audience = {<selectors>...}

platforms = "ios"
platforms = "android"
platforms = "amazon"
platforms = "blackberry"

device_types = "all"
device_types = [<platforms>, <platforms>...]

api_v3 = {
    "audience": <audience>,
    "device_types": <device_types>,
    "notification": {"alert": <string>}
}
"""

from api_object_spec.compile import ApiSpecification
import json

spec = ApiSpecification(api_v3)
result = spec.generate('api_v3')
validates = spec.validate('api_v3', result)

print "The result is:"
for line in json.dumps(result, indent=4).split('\n'):
    print '    ' + line
print "Does this payload validate?", validates

"""
Language:

JSON, with a couple extra items:

NAME = DEFINITION BODY
 ^
 |
 - -can have spaces, numbers, underscores, letters


NAME = DEFINITION BODY
        ^
        |
        |
        ----- A PAIR or a VALUE.

PAIR:
    - "string": VALUE
    - <token>: VALUE
    - <token>

VALUE:
    - JSON Object
    - JSON Array
    - Number, String, Boolean, Null
    - Token

Token:
    - Anything in angle brackets
    - Must match a definition name, or the parser will
      error... eventually.

TODO:

    - Recursive API specifications:

        audience = {OPERATOR: <audience>}
    - Specifying Custom tokens.
    - Why didn't validate? Should identify the expression that caused it to fail.
    - Better stack traces if your specification doesn't parse.
    - sphinx extension
#
# """
