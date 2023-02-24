"""Defining tables of the database."""

from web_site import db
from datetime import datetime
from flask_login import UserMixin


class Author(db.Model):
    """Defining authors table."""

    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    born = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # not saving the image itself to the db, just it's name
    pic = db.Column(db.String(), nullable=True)

    quotes = db.relationship("Quote", backref="author", lazy=True)


class Quote(db.Model):
    """Defining quotes table."""

    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
