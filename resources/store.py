from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):  # we will change some of the methods from
    parser = reqparse.RequestParser()
    # in the following line we define how to parse price. Since we are not defining other arguments,
    # if any exist in the request, we won't parse them, since they are not defined. This is good, because
    # if name for example 'name' would be sent, it would update the name of the item, possibly changing it! thus,
    # using reqparse protects us from unintentional updating
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="The store must have a name")

    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    # @jwt_required()  commented out just for testing purposes
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with name {name} already exists.'}, 400 # bad request

        # data = Store.parser.parse_args()
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the store.'}, 500  # internal server error

        return store.json(), 201  # 201 is created



    # @jwt_required()  commented out just for testing purposes
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

