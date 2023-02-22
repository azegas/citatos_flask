# possible fields - https://wtforms.readthedocs.io/en/3.0.x/fields/
# possible validators - https://wtforms.readthedocs.io/en/3.0.x/validators/
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    SubmitField,
    DateField,
    TextAreaField,
    SelectField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length


# Creating a form class for author
class AddAuthorForm(FlaskForm):
    name = StringField("Author's name", validators=[DataRequired()])
    lastname = StringField("Author's lastname", validators=[DataRequired()])
    born = DateField(
        "When the author was born?", format="%Y-%m-%d", validators=[DataRequired()]
    )
    pic = FileField("A Pic of an Author")
    submit = SubmitField("submit")


# Creating a form class for quote
class AddQuoteForm(FlaskForm):
    author_id = SelectField("Author:", validators=[DataRequired()])
    text = TextAreaField(
        "Quote text",
        validators=[
            DataRequired(),
            Length(max=50, message=("Labai neissiplesk seniuk.")),
        ],
    )
    status = SelectField(
        "Status:",
        choices=[("published", "Published"), ("unpublished", "Unpublished")],
        default="unpublished",
    )
    score = IntegerField(
        "Score",
        validators=[DataRequired()],
    )
    submit = SubmitField("submit")
