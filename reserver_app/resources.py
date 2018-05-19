from flask_restful import Resource, reqparse
from reserver_app.models import UserModel
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt
)
from models import UserModel, RevokedTokenModel

parser = reqparse.RequestParser()
parser.add_argument(
    'username',
    help='This field cannot be blank',
    required=True
)
parser.add_argument(
    'password',
    help='This field cannot be blank',
    required=True
)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} successfully created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        except:
            return {
                'message': 'User was not created due to error'
            }, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {
                'message': 'User {} does not exist'.format(data['username'])
            }, 404

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {
                'message': 'Incorrect credentials!'
            }, 401
        return data


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                'message': 'Access token has been revoked, user was logged out'
            }
        except:
            return {
                'message': 'User was not logged out due to error'
            }, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {
                'message': 'Refresh token has been revoked'
            }
        except:
            return {
                'message': 'Refresh token has not been revoked due to error'
            }, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {
            'message': 'Refreshed token',
            'access_token', access_token
        }


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class ProtectedResourceExample(Resource):
    @jwt_required
    def get(self):
        return {
            'message': 'Seeing this message means you are logged in'
        }
