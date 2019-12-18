from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):  # we will change some of the methods from
    parser = reqparse.RequestParser()
    # in the following line we define how to parse price. Since we are not defining other arguments,
    # if any exist in the request, we won't parse them, since they are not defined. This is good, because
    # if name for example 'name' would be sent, it would update the name of the item, possibly changing it! thus,
    # using reqparse protects us from unintentional updating
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    # @jwt_required()  commented out just for testing purposes
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400 # bad request

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # same as data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500  # internal server error

        return item.json(), 201  # 201 is created



    # @jwt_required()  commented out just for testing purposes
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # @jwt_required()  commented out just for testing purposes
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)  # same as data['price'], data['store_id']
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

