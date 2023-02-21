"""All the routes are here."""

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import os
from web_site.forms import AddAuthorForm
from werkzeug.utils import secure_filename
import uuid

# ---------------------------------------------------------------------------------------
# DB STUFF
# kai duombaze pradeda pilnai veikti, tik tuomet startinam appsa

db = SQLAlchemy()
migrate = Migrate()

# kad nebutu circular imports
from web_site.models import Quote, Author


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


@app.route("/add_author", methods=["GET", "POST"])
def route_add_author():
    """Use form to add add a new author to the database."""
    form = AddAuthorForm()
    # Validate form
    if form.validate_on_submit():
        name = request.form["name"]
        lastname = request.form["lastname"]
        born = request.form["born"]
        hobby = request.form["hobby"]

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

        author = Author(name=name, lastname=lastname, born=born, hobby=hobby, pic=pic)

        flash("Successfully added an author!")
        db.session.add(author)
        db.session.commit()
        return redirect(url_for("route_all_authors"))
    return render_template("add_author.html", form=form)


# --------------------------------------------------------------------


@app.route("/add_quote", methods=["GET", "POST"])
def route_add_quote():
    """Add a new quote to the database."""
    if request.method == "POST":
        text = request.form["text"]
        status = request.form["status"]
        date_created = request.form["date_created"]
        score = request.form["score"]
        author_id = request.form["author_id"]
        quote = Quote(
            text=text,
            status=status,
            date_created=date_created,
            score=score,
            author_id=author_id,
        )
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for("route_all_quotes"))
    authors = Author.query.all()
    return render_template("add_quote.html", authors=authors)


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
    # Retrieve flashed message(all in genereal)
    message = get_flashed_messages()
    # Retrieve all authors from the database
    authors = Author.query.all()
    return render_template("all_authors.html", authors=authors, message=message)


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
