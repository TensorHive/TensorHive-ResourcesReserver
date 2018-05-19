from flask_restful import Resource, reqparse, Api
from reserver_app.models import UserModel
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt
)
from reserver_app.models import UserModel, RevokedTokenModel
from flask import Blueprint

api_v1_users_blueprint = Blueprint('api_v1_users', __name__)
api_v1_users = Api(api_v1_users_blueprint)

class AllUsers(Resource):
    @jwt_required
    def get(self):
        return UserModel.return_all()

    @jwt_required
    def delete(self):
        return UserModel.delete_all()


class ProtectedResourceExample(Resource):
    @jwt_required
    def get(self):
        return {
            'message': 'Seeing this message means you are logged in'
        }

api_v1_users.add_resource(AllUsers, '/users')
api_v1_users.add_resource(ProtectedResourceExample, '/secret')