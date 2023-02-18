"""Simple web app for quotes."""

from web_site import app
from web_site.models import db

if __name__ == "__main__":
    with app.app_context():  # kad db sesiju dalykai nesusipintu
        db.create_all()
    app.run(debug=True)
