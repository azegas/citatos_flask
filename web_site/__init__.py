"""All the routes are here."""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import os


# kai duombaze pradeda pilnai veikti, tik tuomet startinam appsa

db = SQLAlchemy()
migrate = Migrate()

# kad nebutu circular imports
from web_site.models import Quote, Author


# initializing the db and creates the tables
def create_app():
    app = Flask(__name__)  # sukuriame flask instance
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


@app.route("/")
def route_index():
    """Render index page."""
    quotes_data = Quote.query.all()
    if not quotes_data:
        return render_template("no_quotes.html")
    random_quote = random.choice(quotes_data)
    return render_template(
        "index.html",
        random_quote=random_quote,
    )


@app.route("/all_quotes")
def route_all_quotes():
    """Render a list of all quotes."""
    quotes_data = Quote.query.all()
    return render_template("all_quotes.html", quotes_data=quotes_data)


@app.route("/all_authors")
def route_all_authors():
    """Render a list of all authors."""
    authors = Author.query.all()
    return render_template("all_authors.html", authors=authors)


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


@app.route("/add_author", methods=["GET", "POST"])
def route_add_author():
    """Add a new author to the database."""
    if request.method == "POST":
        name = request.form["name"]
        lastname = request.form["lastname"]
        born = request.form["born"]
        hobby = request.form["hobby"]
        author = Author(
            name=name,
            lastname=lastname,
            born=born,
            hobby=hobby,
        )
        db.session.add(author)
        db.session.commit()
        return redirect(url_for("route_all_authors"))
    return render_template("add_author.html")


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
