from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'  # this tells SQLAlchemy how to map to db table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')  # this is like a join between items and stores


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):  # this returns a JSON representation of the model
        return {'name': self.name, 'price': self.price, 'store': self.store_id}

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
