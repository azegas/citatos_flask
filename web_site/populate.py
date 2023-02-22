from web_site import db, app, Author, Quote
from PIL import Image

# --------------------------------------------------------------------
# error message
# RuntimeError: Working outside of application context.
# This typically means that you attempted to use functionality that
# needed the current application. To solve this, set up an application
# context with app.app_context(). See the documentation for more
# information.
# --------------------------------------------------------------------

# chatgpt solution:
# The error message suggests that you are trying to use Flask
# functionality outside of the application context, which is not
# allowed. You need to create an application context before you can
# use Flask-SQLAlchemy.

# To create an application context, you can use the app.app_context()
# method, where app is your Flask application instance. This will
# create the application context and allow you to create the database
# tables.

# creating empty db
with app.app_context():
    db.create_all()

# adding authors
with app.app_context():
    with open(
        "/home/arvydas/Dropbox/src/citatos_flask/web_site/static/images/bill_burr.jpeg",
        "rb",
    ) as f:
        bill_img_data = f.read()
    bill = Author(name="bill", lastname="burr", born=1968, hobby="drums")
    bill.picture = bill_img_data

    nir = Author(name="nir", lastname="eyal", born=1980, hobby="drums")
    silvanus = Author(name="silvanus", lastname="thompson", born=1851, hobby="Maths")
    unknown = Author(name="unknown", lastname="unknown", born=99999, hobby="unknown")
    db.session.add_all([bill, nir, unknown])
    db.session.commit()

# adding quotes
with app.app_context():
    bill_quote = Quote(
        text="Anything worth having in life is just getting through bombing",
        status="published",
        date_created=1999,
        score=100,
        author=bill,
    )
    bill_quote2 = Quote(
        text="Tikrai nebloga quote",
        status="published",
        date_created=1999,
        score=100,
        author=bill,
    )
    nir_quote = Quote(
        text="Slaves to the urgent at the cost of the important",
        status="published",
        date_created=1992,
        score=44,
        author=nir,
    )
    unknown_quote = Quote(
        text="Beautiful things don't ask for attention",
        status="published",
        date_created=2004,
        score=1022,
        author=unknown,
    )
    silvanus_quote = Quote(
        text="What one fool can do, another can",
        status="published",
        date_created=2344,
        score=111,
        author=silvanus,
    )
    db.session.add_all(
        [bill_quote, bill_quote2, nir_quote, unknown_quote, silvanus_quote]
    )
    db.session.commit()
