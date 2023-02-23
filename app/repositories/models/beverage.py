from app.plugins import db


class Beverage(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    price = db.Column(db.Float, nullable=False)
