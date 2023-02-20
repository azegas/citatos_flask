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
    return render_template(
        "index.html",
        quotes_data=quotes_data,
    )


@app.route("/all_quotes")
def route_all_quotes():
    """Render a list of all quotes."""
    quotes_data = Quote.query.all()
    return render_template("all_quotes.html", quotes_data=quotes_data)


@app.route("/all_authors")
def route_all_authors():
    """Render a list of all authors."""
    quotes_data = Quote.query.all()
    return render_template(
        "all_authors.html",
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
