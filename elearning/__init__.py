import os
from flask import Flask, jsonify, request, render_template, flash, redirect
from flask.helpers import url_for
from flask.wrappers import JSONMixin
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

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


db.create_all()

api = Api(elearning, errors=errors)


from elearning.resources.routes import initialize_routes
from elearning.models import User, Class


@elearning.route('/manual/classes/arsifkan/<int:class_id>')
def arsipkan(class_id):
    current_class = Class.query.get(class_id)
    if current_class.archived == True:
        current_class.archived = False
        db.session.commit()
    else:
        current_class.archived = True
        db.session.commit()
        
    return redirect(url_for('semua_class'))


@elearning.route('/manual/classes')
def semua_class():
    active_classes = []
    archived_classes = []

    for cls in Class.query.all():
        if cls.archived == False:
            _active = {}
            _active['Classname'] = cls.classname
            _active['class_id'] = cls.class_id
            active_classes.append(_active)
        if cls.archived == True:
            _archive = {}
            _archive['Classname'] = cls.classname
            _archive['class_id'] = cls.class_id
            archived_classes.append(_archive)

    return render_template('template_class.html', active_classes=active_classes, archived_classes=archived_classes)

@login.user_loader
def load_user(id):
    return User.query.get(id)
    
initialize_routes(api)