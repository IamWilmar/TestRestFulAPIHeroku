from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

#DEFINIR API
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

#DEFINIR COMO SE VA A ACCEDER A LOS RESORUCES
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') #http://127:0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')          #http://127.0.0.1:5000/items
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

#CORRER LA API
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
