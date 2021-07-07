import os
from flask import Flask, request, render_template, redirect, flash
from flask.helpers import url_for
from flask_login.utils import login_required
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_cors import CORS

from elearning.resources import errors
from elearning.config import Config


UPLOAD_FOLDER = os.getcwd()

elearning = Flask(__name__)
elearning.config.from_object(Config)
elearning.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(elearning)
login = LoginManager(elearning)
db = SQLAlchemy(elearning)

db.create_all()

api = Api(elearning, errors=errors)


from elearning.resources.routes import initialize_routes
from elearning.models import User, Class


@elearning.route('/manual/classes/arsifkan/<int:class_id>/')
def arsipkan(class_id):
    """Fungsi akan dijalankan ketika salah satu kelas di arsipkan secara manual (bukan melalui API)"""
    current_class = Class.query.get(class_id)
    if current_class.archived == True:
        current_class.archived = False
        db.session.commit()
    else:
        current_class.archived = True
        db.session.commit()
    return redirect(url_for('semua_class'))

@elearning.route('/manual/classes/')
# @login_required
def semua_class():
    """Memisahkan class yang aktif dan yang diarsif secara manual (bukan melalui API)"""
    if current_user.is_anonymous:
        flash("Kamu belum login!")
        return redirect(url_for('login'))

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


@elearning.route('/manual/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("Kamu udah login sebelumnya!!!")
        return redirect(url_for('semua_class'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email tidak ditemukan')
            return redirect(url_for('login'))
        if not user.check_password(password):
            flash('Password anda salah')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('semua_class'))

    return render_template('login.html')
        
@elearning.route('/manual/logout')
def logout():
    logout_user()
    flash('Kamu udah keluar!!!')
    return redirect(url_for('login'))


initialize_routes(api)