"""All the routes are here."""

from flask import Flask, render_template, request, redirect, url_for
from web_site.data.quotes_data import quotes_data
from web_site.data.authors import authors

app = Flask(__name__)


@app.route("/")
def index():
    """Render index page."""
    return render_template("index.html")


@app.route("/all_quotes")
def all_quotes():
    """
    Render a list of all quotes.

    quotes = how I use it in template, how I serve data TO the template
    data = how it is actually named in the imported file.
    """
    return render_template("all_quotes.html", quotes=quotes_data)


# quote_title taken from all_quotes.html is being used in the url
@app.route("/all_quotes/<string:quote_title>")
# for this function I must serve quote_title from where I am calling it, in this case - from all_quotes.html
def quote(quote_title):
    """
    Render a single quote upon choosing a single quote.

    quote_title = I get it from all_quotes html page, using it for this function
    title = name I assign to pavadinimas and serve to function
    quotes = how I use it in template, how I serve data TO the template
    data = how it is actually named in the imported file.
    """
    return render_template("single_quote.html", title=quote_title, quote=quotes_data)


@app.route("/all_authors")
def all_authors():
    """Render a list of all authors."""
    return render_template("all_authors.html", authors=quotes_data)


@app.route("/all_authors/<string:single_author>")
def author(single_author):
    """
    Render a single author page using two data sources.

    single_author = is what I receive from all_authors
    authors = database name that I imported
    autoriaus_vardas = my assigned value to the single_author
    autoriaus_info = my assigned value to the database of authors.py, must be used in
    """
    return render_template(
        "single_author.html",
        autoriaus_vardas=single_author,
        autoriaus_info=authors,
        quotes=quotes_data,
    )


@app.route("/add_quote", methods=["GET", "POST"])
def add_quote():
    """Paaiskinimas."""
    if request.method == "POST":
        date = request.form["date"]
        autorius = request.form["autorius"]
        tekstas = request.form["tekstas"]
        pavadinimas = request.form["pavadinimas"]
        quotes_data.append(
            {
                "data": date,
                "autorius": autorius,
                "pavadinimas": pavadinimas,
                "tekstas": tekstas,
                "status": "published",
            }
        )
        return redirect(url_for("all_quotes"))
    return render_template("add_quote.html")
