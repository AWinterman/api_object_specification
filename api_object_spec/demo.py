"""
            ==========================
            Json Object Specification
            ==========================

   Specifying JSON objects in a simple, human readable format.

            Andrew Winterman, Marc Sciglimpaglia
"""




































"""
http://eng-docs.prod.urbanairship.com/docs/api-v3/en/latest/#api-endpoints

This is pretty good, you can read it, and get some idea of what the spec should
be" But it's up to you to keep the full specification in your head As the
specification grows in complexity, this can become difficult.

For example: notification.ios.alert

         "alert" - Override the alert value provided at the top level, if any.
         May be a JSON string or an object which conforms to Apple's spec (see
         Table 3-2 in the APNS Docs).

I was on the web team when we found out about this, years (?) after it had been
implemented.

The website needs to support the FULL SET OF POSSIBLE API PAYLOADS.

As do API consumers.

Producers should be able to validate correctness when they generate api
payloads.
"""



















"""
Goal:
     - Write a DSL for specifying JSON objects.
     - Keep it easy to read, easy to write.
     - Keep the rules simple.
     - Compile the DSL into an API generator for
       fuzzing, and a validator

"""


api_v3 = """
uuid = "6086e075-65cb-4702-9bfa-f898bf5267ab"
uuid = "c41d36ab-583a-4f4e-902c-e11c9ae30d42"
uuid = "2eff688b-6d3d-466c-ad87-c9fdf1ab45ce"

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
device_types = [<platforms>...]

api_v3 = {
    "audience": <audience>,
    "device_types": <device_types>
}
"""
#
from compile import ApiSpecification
import json

spec = ApiSpecification(api_v3)

print spec.generate('api_v3')

print json.dumps(spec.generate('api_v3'), indent=4)






















#
# """
# print "Example:"
# print "Russell and Graham's hackweek project is a plugin for reading reactor messages with WireShark"
# print "It get's configured with an ENORMOUS json object."
# """
#
# from example import full
#
# print full
#
# import os
# import json
#
# from compile import ApiSpecification
# from examples import *
#
# print json.dumps(full, indent=4)
# print JSL
# rpc_spec = ApiSpecification(JSL)
#
#
# print json.dumps(bonestorm_spec, indent=4)
# print rpc_spec.validate('rpc', bonestorm_spec), '<----- the whole bonestorm spec!'
#
# print json.dumps(bonestorm_spec['bonestorm'])
# print rpc_spec.validate('payload_handler', bonestorm_spec['bonestorm']['request_payload_handler'])
#
# print rpc_spec.validate('rpc', json.loads(argon_example)), '<------ argon turns out to be really complicated'
#
# print rpc_spec.validate('payload_handler', json.loads(argon_example)['argon'][
#     'response_payload_handler']), '<--- argon response payload handler'
# print rpc_spec.validate('payload_handler', json.loads(argon_example)['argon']['response_payload_handler']['handlers'][
#     'payload']), '<--- argon response payload handler'
#
# m = json.loads(argon_example)['argon']['response_payload_handler']['handlers']['payload']['message_map']
#
# print json.dumps(m, indent=4)
# print rpc_spec.definitions['payload_handler']
# print rpc_spec.validate('message_map', m)
#
#
