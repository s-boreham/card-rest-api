from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from models.card import CardModel
from models.realm import RealmModel

class Card(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('cost',
                        type=int,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('ability',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    def get(self, color, name):
        realm = RealmModel.find_by_color(color)
        if realm is None:
            return {'message': "Realm with color '{}' does not exist yet".format(color)}, 400

        card = CardModel.find_by_name(name)
        if card:
            return card.json()
        return {'message': 'Card not found'}, 404

    @jwt_required()
    def post(self, color, name):
        if CardModel.find_by_name(name):
            return {'message': "A card with name '{}' already exists".format(name)}, 400

        realm = RealmModel.find_by_color(color)
        if realm is None:
            return {'message': "Realm with color '{}' does not exist yet".format(color)}, 400
        
        data = Card.parser.parse_args()

        card = CardModel(realm.id, **data)

        try:
            card.save_to_db()
        except:
            return {'message': 'An error occured inserting the card'}, 500

        return card.json(), 201

    @jwt_required()    
    def put(self, color, name):        
        data = Card.parser.parse_args()

        card = CardModel.find_by_name(name)

        if card is None:
            card = CardModel(**data)
        else:
            card.cost = data['cost']
            card.ability = data['ability']

        card.save_to_db()

        return card.json()

    @jwt_required()
    def delete(self, color, name):
        card = CardModel.find_by_name(name)
        
        if card:
            card.delete_from_db()

        return {'message': 'Card deleted'}


class CardList(Resource):
    def get(self, color):
        realm = RealmModel.find_by_color(color)
        if realm is None:
            return {'message': "Realm with color '{}' does not exist yet".format(color)}, 400
                
        return {'cards': [card.json() for card in CardModel.find_all_by_realm(realm.id)]}, 200