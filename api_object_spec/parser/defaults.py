import model

constraints = (
    model.ObjectRefConstraint("object"),
    model.StringRefConstraint("string"),
    model.NumberRefConstraint("number"),
    model.BooleanRefConstraint("boolean")
)

definitions = {c.name: [model.Definition(name=c.name, constraints=c)] for c in constraints}
