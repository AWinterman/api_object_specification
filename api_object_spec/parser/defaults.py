import model
from collections import defaultdict

constraints = (
    model.ObjectRefConstraint("object"),
    model.StringRefConstraint("string"),
    model.NumberRefConstraint("number"),
    model.BooleanRefConstraint("boolean")
)

definitions = defaultdict(list, {c.name: [model.Definition(name=c.name, constraints=c)] for c in constraints})
