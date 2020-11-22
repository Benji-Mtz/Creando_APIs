from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        """ for item in items:
            if item['name'] == name:
                return item """
        # next recorre a items retornando una lista pero rompe el ciclo si no hay datos
        item = next( filter( lambda x: x['name'] == name, items), None )

        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        if next( filter( lambda x: x['name'] == name, items), None ):
            return {'message': "An item with name '{}' already exist.".format(name)}, 400

        #force=True, no necesita un content-type-header
        #silent=True es similar a focer pero regresa None
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        # global indica que la variable local sera ahora global
        global items
        #aqui se crear una lista nueva filtrando todo menos 1 item con x nombre
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "Item deleted"}

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



if __name__ == '__main__':
    app.run(port=5000, debug=True)
 