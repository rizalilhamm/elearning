import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from elearning.config import Config

elearning = Flask(__name__)
elearning.config.from_object(Config)
login = LoginManager(elearning)
db = SQLAlchemy(elearning)
api = Api(elearning)

from elearning.resources.routes import initialize_routes
from elearning.models import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
initialize_routes(api)