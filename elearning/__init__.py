import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from elearning.resources import errors
from elearning.config import Config

UPLOAD_FOLDER = os.getcwd()

elearning = Flask(__name__)
elearning.config.from_object(Config)
elearning.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login = LoginManager(elearning)
db = SQLAlchemy(elearning)
migrate = Migrate(elearning, db)
api = Api(elearning, errors=errors)

from elearning.resources.routes import initialize_routes
from elearning.models import User


@login.user_loader
def load_user(id):
    return User.query.get(id)
    
initialize_routes(api)