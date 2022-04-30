from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    decks = db.relationship('Decks')


class Decks(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_name = db.Column(db.String(10000))
    cards = db.relationship('Cards')


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id'))
    NL = db.Column(db.String(10000))
    TL_word = db.Column(db.String(10000))
    NL_word = db.Column(db.String(10000))
    is_recalled = db.Column(db.Boolean())  # boolean, true if the card wad recalled, false if not
    interval = db.Column(db.Integer)  # amount of days since the card was last recalled
    date = db.Column(db.String(10000))  # date of the last recall 
    