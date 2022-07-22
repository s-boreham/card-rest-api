from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from db import db

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.realm import Realm, RealmList
from resources.card import Card, CardList

from blocklist import BLOCKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'shamrobe' # app.config['JWT_SECRET_KEY'] 
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload: dict):
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def invalid_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401    

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(Realm, '/realm/<string:color>')
api.add_resource(RealmList, '/realms')

api.add_resource(Card, '/realm/<string:color>/card/<string:name>')
api.add_resource(CardList, '/realm/<string:color>/cards')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)