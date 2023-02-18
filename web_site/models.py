from web_site import db


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(80), nullable=True)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
        self.city = city

    def __repr__(self):
        return f"{self.name} - {self.email}, from {self.city}"
