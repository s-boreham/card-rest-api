import sqlite3
from db import db

class CardModel(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    cost = db.Column(db.Integer())
    ability = db.Column(db.String(80))

    realm_id = db.Column(db.Integer,db.ForeignKey('realms.id'))
    realm = db.relationship('RealmModel')

    def __init__(self, realm_id, name, cost=1, ability=''):
        self.name = name
        self.cost = cost
        self.ability = ability
        self.realm_id = realm_id

    def json(self):
        return{
            'name': self.name,
            'realm': self.realm.color,
            'cost': self.cost,
            'ability': self.ability
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all() 

    @classmethod
    def find_all_by_realm(cls, realm_id):
        return cls.query.filter_by(realm_id=realm_id) 