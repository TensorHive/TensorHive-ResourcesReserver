from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import datetime as dt

app = Flask(__name__)
# TODO Store configuration in separate file, especially secret_key. Shift responsibility to config.py or something
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jwt-some-secret'

# Default values
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = dt.datetime.utcnow() + dt.timedelta(minutes=15)
#app.config['JWT_REFRESH_TOKEN_EXPIRES'] = dt.datetime.utcnow() + dt.timedelta(days=30)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['BUNDLE_ERRORS'] = True



db = SQLAlchemy(app)
jwt = JWTManager(app)

from reserver_app import views, models, resources
from reserver_app.auth.views import auth_blueprint
from reserver_app.api.v1.users import api_v1_users_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(api_v1_users_blueprint, url_prefix='/api/v1')

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def is_token_on_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)