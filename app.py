import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


"""
The Resource and Api libraries allow us to create true RESTful API's that adhere to the REST priniples.
Resources are things such as users, stores, items, etc. 

All resources that we define are classes.
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This just turns off the flask SQLAlchemy mod tracker
# but not the SQLAlchemy mod tracker
app.secret_key = 'somesecretkeyb'
api = Api(app)

# JWT() creates a new endpoint named /auth. When we call /auth, we send it a username and password. The JWT extension
# gets the username and password and sends it over to the authenticate() function which takes in a username and
# password, and looks up the user by username and then it will compare it to the password that we will receive
# through the /auth endpoint. If they match then it returns the user which kind of becomes the identity. Next, the /auth
# endpoint returns a jwt token. We will use the JWT token to send it to the next request we make. When we send the
# JWT token, then it calls the identity() function, which then uses the JWT token to get the userid and then
# returns the correct user.
# NOTE: we add the @jwt_required decorator before the get() in the Item resource, below.

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')  # this lists the route for resource Item
api.add_resource(ItemList, '/items')  # this lists the route for resource Items
api.add_resource(UserRegister, '/register')  # this lists the route for resource UserRegister
api.add_resource(Store, '/store/<string:name>')  # this lists the route for resource Store
api.add_resource(StoreList, '/stores')  # this lists the route for resource Stores

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
