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
    PasswordField,
)
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError


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


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(min=4, max=20),
        ],  # later it hashes, so setting it here to 20 and 80 in the model. It hashes it to put to db
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")

    # can not reach User model for some reason to validate if it already exists or not
    # def validate_username(self, username):
    #     existing_user_username = User.query.filter_by(username=username.data).first()
    #     if existing_user_username:
    #         raise ValidationError(
    #             "That username already exists, choose a different one"
    #         )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(min=4, max=20),
        ],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")
