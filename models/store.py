from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'  # this tells SQLAlchemy how to map to db table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # lazy building of items because it could be costly

    def __init__(self, name):
        self.name = name

    def json(self):  # this returns a JSON representation of the model
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}  # if lazy=d\'dynamic' then
        # we must add .all() to self.items because self.items is no longer a list of items, but it is now a query
        # builder that has the ability to look in to the items table. So we won't look in to the table untill we call
        # the json() method, and creating stores is now simple.

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name LIMIT 1
        # (the 2nd name is the argument). In addition, the selected data is converted in to an ItemModel object
        # that has self.name and self.price

    def save_to_db(self):  # this works for both insert and update (upsert)
        db.session.add(self)  # this will insert from self.name and self.price.
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
