import sqlite3
from db import db

class RealmModel(db.Model):
    __tablename__ = 'realms'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(80))
    bonus = db.Column(db.String(80))

    cards = db.relationship('CardModel', lazy='dynamic')

    def __init__(self, color, bonus=''):
        self.color = color
        self.bonus = bonus

    def json(self):
        return{
            'color': self.color,
            'bonus': self.bonus
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_color(cls, color):
        return cls.query.filter_by(color=color).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all() 