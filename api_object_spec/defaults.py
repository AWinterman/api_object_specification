import model
from collections import defaultdict

constraints = (
    model.ObjectRef("object"),
    model.StringRef("string"),
    model.NumberRef("number"),
    model.BooleanRef("boolean")
)

definitions = defaultdict(list, {c.name: [c] for c in constraints})