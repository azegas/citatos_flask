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


class AddAuthorForm(FlaskForm):
    """Creating a form class for new author."""

    name = StringField("Author's name:", validators=[DataRequired()])
    lastname = StringField("Author's lastname:", validators=[DataRequired()])
    born = DateField(
        "When the author was born?", format="%Y-%m-%d", validators=[DataRequired()]
    )
    pic = FileField("Add a picture of an author:")
    submit = SubmitField("Submit")


class AddQuoteForm(FlaskForm):
    """Creating a form class for new quote."""

    author_id = SelectField(
        "Author:",
        validators=[DataRequired(), Length(max=50)],
    )
    text = TextAreaField(
        "Quote text:",
        validators=[DataRequired(), Length(max=1000)],
    )
    status = SelectField(
        "Status:",
        choices=[("published", "Published"), ("unpublished", "Unpublished")],
        default="unpublished",
    )
    score = IntegerField(
        "Score:",
        validators=[DataRequired()],
    )
    submit = SubmitField("submit")
