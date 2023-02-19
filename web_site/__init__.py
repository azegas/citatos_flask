"""All the routes are here."""

from flask import Flask, render_template, request, redirect, url_for
from web_site.data.quotes_data import quotes_data
from web_site.data.authors_data import authors_data
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import os


# kai duombaze pradeda pilnai veikti, tik tuomet startinam appsa

db = SQLAlchemy()
migrate = Migrate()

# kad nebutu circular imports
from web_site.models import Quote, Author


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


def filter_only_authors():
    """Filter authors."""
    filtered_authors = set()  # Karina
    for author in quotes_data:
        filtered_authors.add(author["autorius"])
    return filtered_authors


filter_only_authors = filter_only_authors()


# --------------------------------------------------------------------


def generate_random_post():
    """Generate a random post."""
    random_post = random.choice(quotes_data)
    return random_post


random_post = generate_random_post()

# --------------------------------------------------------------------


@app.route("/")
def route_index():
    """Render index page."""
    return render_template(
        "index.html",
        quotes_data=quotes_data,
        filter_only_authors=filter_only_authors,
        random_post=random_post,
    )


@app.route("/all_quotes")
def route_all_quotes():
    """
    Render a list of all quotes.

    quotes = how I use it in template, how I serve data TO the template
    data = how it is actually named in the imported file.
    """
    return render_template("all_quotes.html", quotes_data=quotes_data)


# quote_title taken from all_quotes.html is being used in the url
@app.route("/all_quotes/<string:quote_title>")
# for this function I must serve quote_title from where I am calling
# it, in this case - from all_quotes.html
def route_single_quote(quote_title):
    """Render a single quote upon choosing a single quote."""
    return render_template(
        "single_quote.html", quote_title=quote_title, quotes_data=quotes_data
    )


@app.route("/all_authors")
def route_all_authors():
    """Render a list of all authors."""
    for author in quotes_data:
        filter_only_authors.add(author["autorius"])
    return render_template(
        "all_authors.html",
        quotes_data=quotes_data,
        filter_only_authors=filter_only_authors,
    )


@app.route("/all_authors/<string:single_author>")
def route_single_author(single_author):
    """Render a single author page using two data sources."""
    return render_template(
        "single_author.html",
        single_author=single_author,
        authors_data=authors_data,
        quotes_data=quotes_data,
    )


@app.route("/add_quote", methods=["GET", "POST"])
def route_add_quote():
    """Paaiskinimas."""
    if request.method == "POST":
        date = request.form["date"]
        autorius = request.form["autorius"]
        tekstas = request.form["tekstas"]
        pavadinimas = request.form["pavadinimas"]
        balai = request.form["balai"]
        quotes_data.append(
            {
                "data": date,
                "autorius": autorius,
                "pavadinimas": pavadinimas,
                "tekstas": tekstas,
                "status": "published",
                "balai": int(balai),
            }
        )
        return redirect(url_for("route_all_quotes"))
    return render_template("add_quote.html")
