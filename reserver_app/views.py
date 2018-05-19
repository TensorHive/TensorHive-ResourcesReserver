from reserver_app.run import app
from flask import jsonify

@app.route('/')
def index():
    return jsonify({'msg': 'Unprotected access'})