"""All the routes are here."""

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import os
from web_site.forms import AddAuthorForm, AddQuoteForm, LoginForm, RegisterForm
from werkzeug.utils import secure_filename
import uuid
from flask_bcrypt import Bcrypt
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

# ---------------------------------------------------------------------------------------
# DB STUFF
# kai duombaze pradeda pilnai veikti, tik tuomet startinam appsa

db = SQLAlchemy()
migrate = Migrate()

# kad nebutu circular imports
from web_site.models import Quote, Author, User


# initializing the db and creates the tables
def create_app():
    app = Flask(__name__)  # creating a Flask Instance
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "db.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)  # kuriame appse bus db inicializuota
    migrate.init_app(app, db)
    return app


app = create_app()

# --------------------------------------------------------------------
# AUTHENTICATION stuff

# hashing
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# user loader callback
# used to reload the user object from the user id stored in the session?
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --------------------------------------------------------------------
# IMG Stuff
app.config["UPLOAD_FOLDER"] = "static/images"


# --------------------------------------------------------------------
# FORM STUFF

# CSRF token cross site request forgery?

# creates a little secret key on the form that then later syncs behind
# the scenes with another secret key. CSRF token will use the secret key.
# this below is Zygimantas way of generating a secret key.


SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
# print(SECRET_KEY)

# --------------------------------------------------------------------
# CREATING ROUTES


@app.route("/dashboard/add_author", methods=["GET", "POST"])
@login_required
def route_add_author():
    """Use form to add add a new author to the database."""
    form = AddAuthorForm()
    # Validate form
    if form.validate_on_submit():
        name = request.form["name"]
        lastname = request.form["lastname"]
        born = request.form["born"]

        # -----------------------------------------------------------
        # Images stuff
        # add uuid "Upload Profile Picture - Flask Fridays #38" in
        # case multiple users will be adding images and there is a
        # risk they will use same filenames, like "profile.jpg"

        # fetch FULL IMAGE, memetype, filename, etc from the form
        pic = request.files["pic"]
        # Grab image NAME only, making sure it is secure by checking
        # the filename(SQL injection stuff)
        pic_filename = secure_filename(pic.filename)
        # set UUID to the pic_filename
        pic_name_with_uuid = str(uuid.uuid1()) + "_" + pic_filename
        # save that IMAGE with uuid prefix to the static/images folder
        pic.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                pic_name_with_uuid,
            )
        )
        # change the FULL IMAGE to a string with uuid to save to db
        pic = pic_name_with_uuid

        # -----------------------------------------------------------

        author = Author(name=name, lastname=lastname, born=born, pic=pic)

        db.session.add(author)
        db.session.commit()
        return redirect(url_for("route_all_authors"))
    return render_template("add_author.html", form=form)


# --------------------------------------------------------------------


@app.route("/dashboard/add_quote", methods=["GET", "POST"])
@login_required
def route_add_quote():
    """Use form to add add a new author to the database."""
    form = AddQuoteForm()
    authors = Author.query.all()
    choices = [(author.id, f"{author.name} {author.lastname}") for author in authors]
    form.author_id.choices = choices
    if form.validate_on_submit():
        author_id = request.form["author_id"]
        text = request.form["text"]
        status = request.form["status"]
        score = request.form["score"]
        quote = Quote(
            author_id=author_id,
            text=text,
            status=status,
            score=score,
        )
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for("route_all_quotes"))
    return render_template("add_quote.html", form=form)


# --------------------------------------------------------------------


@app.route("/")
def route_index():
    """Render index page."""
    quotes_data = Quote.query.all()

    if not quotes_data:
        return render_template("no_quotes.html")

    # testffing built in jinja filters
    # https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-builtin-filters
    string = "A <strong>RANDOM</strong> QUOTE:"

    random_quote = random.choice(quotes_data)
    return render_template("index.html", random_quote=random_quote, string=string)


# --------------------------------------------------------------------


@app.route("/all_quotes")
def route_all_quotes():
    """Render a list of all quotes."""
    quotes_data = Quote.query.all()
    return render_template("all_quotes.html", quotes_data=quotes_data)


# --------------------------------------------------------------------


@app.route("/all_authors")
def route_all_authors():
    """Render a list of all authors."""
    # Retrieve all authors from the database
    authors = Author.query.all()
    return render_template("all_authors.html", authors=authors)


# --------------------------------------------------------------------


@app.route("/all_authors/<string:first_last_name>/quotes")
def route_single_author(first_last_name):
    """Render a list of quotes by a specific author."""
    # split the name into first and last parts
    name, lastname = first_last_name.split("_")
    # find the author based on first and last name
    author = Author.query.filter_by(name=name, lastname=lastname).first_or_404()
    quotes_data = author.quotes
    return render_template("single_author.html", author=author, quotes_data=quotes_data)


# --------------------------------------------------------------------
# CREATING CUSTOM ERROR PAGES
# https://www.presslabs.com/how-to/error-pages/#what-are-error-pages


# Invalid URL
# if I don't pass the error code at the end, terminal shows 200
@app.errorhandler(404)
def page_not_found(e):
    return (render_template("errors/404.html"), 404)


# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500


# --------------------------------------------------------------------
# CREATING AUTHENTICATION


@app.route("/register", methods=["GET", "POST"])
def route_register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("route_login"))

    return render_template("authentication/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def route_login():
    # check if user is already logged in and if yes - redirect to dashboard instead of the login page
    if current_user.is_authenticated:
        return redirect(url_for("route_dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        # check if the user is in the database or not
        user = User.query.filter_by(username=form.username.data).first()
        # if they are, we will check their password hash
        if user:
            # see if the password that we wrote matches the hashed one in our db
            if bcrypt.check_password_hash(user.password, form.password.data):
                # if passwords mached, then login and redirect
                login_user(user)
                return redirect(url_for("route_dashboard"))
        # if the user is not in the database or the password is incorrect, then redirect them to the login page
    return render_template("authentication/login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def route_logout():
    logout_user()
    return redirect(url_for("route_login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def route_dashboard():
    return render_template("authentication/dashboard.html")
