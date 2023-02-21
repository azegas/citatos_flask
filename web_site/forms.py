# possible fields - https://wtforms.readthedocs.io/en/3.0.x/fields/
# possible validators - https://wtforms.readthedocs.io/en/3.0.x/validators/
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length


# Creating a form class
class AddAuthorForm(FlaskForm):
    name = StringField("Author's name", validators=[DataRequired()])
    lastname = StringField("Author's lastname", validators=[DataRequired()])
    born = DateField(
        "When the author was born?", format="%Y-%m-%d", validators=[DataRequired()]
    )
    hobby = TextAreaField(
        "Author's hobby",
        validators=[
            DataRequired(),
            Length(max=5, message=("Labai neissiplesk seniuk.")),
        ],
    )
    submit = SubmitField("submit")
