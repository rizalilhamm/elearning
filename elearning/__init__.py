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


user_email_domain = ['lecture.ar-raniry.ac.id', 'student.ar-raniry.ac.id']
@elearning.route('/manual-register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_level = None
        
        if (firstname.replace(' ', '') or lastname.replace(' ', '') or email or password) == '':
            flash('Semua field wajib diisi!')
            return redirect(url_for('register'))
        
        _, email_domain = email.split('@')
        for i in range(len(user_email_domain)):
            if email_domain == user_email_domain[i]:
                if i == 0:
                    user_level = 1
                elif i == 1:
                    user_level = 2
                break
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar coba yang lain')
            return redirect(url_for('register'))

        if user_level == None:
            flash('Email tidak diizinkan')
            return redirect(url_for('register'))
            
        if (password != confirm_password) or (len(password) != len(confirm_password)):
            flash('Password harus sama')
            return redirect(url_for('register'))
        
        new_user = User(firstname=firstname, lastname=lastname, email=email, user_level=user_level)
        new_user.hash_password()
        db.session.add(new_user)
        db.session.commit()
        flash('Register Berhasil, register another email!')
        return redirect(url_for('register'))

    return render_template('register.html')

db.create_all()

api = Api(elearning, errors=errors)


from elearning.resources.routes import initialize_routes
from elearning.models import User


@login.user_loader
def load_user(id):
    return User.query.get(id)
    
initialize_routes(api)