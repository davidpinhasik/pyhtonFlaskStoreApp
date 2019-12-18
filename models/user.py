import sqlite3
from db import db


class UserModel(db.Model):
    # This tells SQLAlchemy the name of the db table to sync our object with
    __tablename__ = 'users'

    # this tells SQLAlchemy the column names and info of the db columns to sync
    # The class properties (self.id, etc.) must match the names mapped to SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  #SQLAlchemy converts it to a UserModel object


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()  #SQLAlchemy converts it to a UserModel object

