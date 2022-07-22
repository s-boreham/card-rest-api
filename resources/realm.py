from flask_restful import Resource, reqparse
from flask_jwt_extended import ( 
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from models.realm import RealmModel

class Realm(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('color',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('bonus',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )

    def get(self, color):
        realm = RealmModel.find_by_color(color)
        if realm:
            return realm.json()
        return {'message': 'Realm not found'}, 404

    @jwt_required()
    def post(self, color):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
            
        if RealmModel.find_by_color(color):
            return {'message': "A realm with color '{}' already exists".format(color)}, 400

        data = Realm.parser.parse_args()

        realm = RealmModel(**data)

        try:
            realm.save_to_db()
        except:
            return {'message': 'An error occured inserting the realm'}, 500

        return realm.json(), 201

    @jwt_required()    
    def put(self, color):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        data = Realm.parser.parse_args()

        realm = RealmModel.find_by_color(color)

        if realm is None:
            realm = RealmModel(**data)
        else:
            realm.bonus = data['bonus']

        realm.save_to_db()

        return realm.json()

    @jwt_required(fresh=True)
    def delete(self, color):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        
        realm = RealmModel.find_by_color(color)
        
        if realm:
            realm.delete_from_db()

        return {'message': 'Realm deleted'}


class RealmList(Resource):
    def get(self):
        return {'realms': [realm.json() for realm in RealmModel.find_all()]}, 200