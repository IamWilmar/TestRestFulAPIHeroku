
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

    #DEFINIR LOS METODOS QUE VA A ACEPTAR
    #Version 0.1

    #codes
    #404 not found
    #200 succesful get
    #201 succesfully created
    #202 similar to 201 but when we are delay ing the creation
    #400 Bad request
    #500 internal server error

#DEFINIR LOS RESORUCES
class Item(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return{'message':'Item not found'}, 404
        

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name {} already exist".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message' : 'An error ocurred  inserting the item'}, 500
        return item.json(), 201

    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}

    #create or update
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:    
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        #return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [x.json() for x in ItemModel.query.all()]}
