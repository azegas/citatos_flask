"""Defining tables of the database."""

from web_site import db
from datetime import datetime


class Author(db.Model):
    """Defining authors table."""

    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    born = db.Column(db.Integer, nullable=False)
    hobby = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # not saving the image itself to the db, just it's name
    pic = db.Column(db.String(), nullable=True)

    quotes = db.relationship("Quote", backref="author", lazy=True)


class Quote(db.Model):
    """Defining quotes table."""

    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # tag
    # location (vipassana, myanmar, other place)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
