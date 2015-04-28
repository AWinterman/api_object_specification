import model
from collections import defaultdict

import rstr
import re

import uuid

class UUID(model.Ref):
    def reify(self):
        return str(uuid.uuid4())

    def _match(self, other):
        try:
            uuid.UUID(other)
            return True
        except Exception:
            return False

constraints = (
    model.ObjectRef("object"),
    model.StringRef("string"),
    model.NumberRef("number"),
    model.BooleanRef("boolean"),
    UUID("uuid"),
)

definitions = defaultdict(list, {c.name: [c] for c in constraints})