import model

constraints = (
    model.ObjectRefConstraint("object"),
    model.StringRefConstraint("string"),
    model.NumberRefConstraint("number"),
    model.BooleanRefConstraint("boolean")
)
