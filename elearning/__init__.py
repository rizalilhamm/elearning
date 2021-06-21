import os
from flask import Flask, jsonify, request
from flask.wrappers import JSONMixin
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS, cross_origin

from elearning.resources import errors
from elearning.config import Config

UPLOAD_FOLDER = os.getcwd()

elearning = Flask(__name__)
elearning.config.from_object(Config)
elearning.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(elearning)
login = LoginManager(elearning)
login.login_view = '/account/login'
login.login_message = 'You have to login to access class'
db = SQLAlchemy(elearning)

@elearning.route('/account/getaja', methods=['POST', 'GET'])
def get_aja():
    return jsonify({
        'data': 'Kasmadi Ramadhan'
    })

db.create_all()

api = Api(elearning, errors=errors)


from elearning.resources.routes import initialize_routes
from elearning.models import User

# from elearning.resources.manualauth import registerManual, loginManual, logoutManual


@login.user_loader
def load_user(id):
    return User.query.get(id)
    
initialize_routes(api)