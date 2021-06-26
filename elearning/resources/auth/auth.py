from flask import Response, request, jsonify
from flask_restful import Resource
from flask_login import current_user, login_required, login_user, logout_user

from elearning.models import User
from elearning import db

user_email_domain = ['lecture.ar-raniry.ac.id', 'student.ar-raniry.ac.id']
class SignupResource(Resource):
    def post(self):
        """ User level:
            0. Admin
            1. Lecturer
            2. Student """
        if current_user.is_authenticated:
            return jsonify({
                'User_id': current_user.id,
                'Message': 'User logged in',
                'Firstname': current_user.firstname,
                'Lastname': current_user.lastname,
                'Status': 200
            })

        if request.method == 'POST':
            if 'firstname' or 'lastname' or 'email' or 'password' or 'confirm_password' not in request.form:
                return jsonify({
                    'Message': 'All field is required!',
                    'Status': 400
                })

            firstname, lastname, email = request.form['firstname'], request.form['lastname'], request.form['email']
            password, confirm_password = request.form['password'], request.form['confirm_password']
            user_level = None
           
            if User.query.filter_by(email=email).first():
                return jsonify({
                    'Message': 'Email has been registered, try another one',
                    'Status': 404
                    })
            
            if (password != confirm_password) or (len(password) != len(confirm_password)):
                return jsonify({
                    'Message': 'Password is not same!',
                    'Status': 404
                })

            _, email_domain = email.split('@') 
            for i in range(len(user_email_domain)):
                if email_domain == user_email_domain[i]:
                    if i == 0:
                        user_level = 1
                    elif i == 1:
                        user_level = 2
                    break

            if user_level == None:
                return jsonify({
                    'Message': 'Email not allowed to register',
                    'Status': 404
                })

            new_user = User(firstname=firstname, lastname=lastname, email=email, password=password, user_level=user_level)
            new_user.hash_password()
            
            db.session.add(new_user)
            db.session.commit()

            return jsonify(
                {
                    'User_id': new_user.id,
                    'Username': '{} {}'.format(firstname, lastname),
                    'Status': 200
                }
            )

        # except Exception as e:
            # return jsonify({"message": "Masih ada yang salah"})   

class LoginResource(Resource):
    def post(self):
        """ User login with email that registered before """
        if current_user.is_authenticated:
            return jsonify({
                'User_id': current_user.id,
                'Message': 'User logged in',
                'Firstname':'{} {}'.format(current_user.firstname, current_user.lastname),
                'Status': 200
            })


        if request.method == 'POST':
            if ('email' not in request.form) or ('password' not in request.form):
                return jsonify({
                    'Message': 'Email and Password are required!',
                    'Status': 400
                })
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return jsonify({
                    'Message': 'invalid email or password!',
                    'Status': 400
                })
            
            login_user(user)
            return jsonify({
                    'User_id': user.id,
                    'Username': user.firstname + ' ' + user.lastname,
                    'Status': 200
            })

    def get(self):
        return jsonify({
            'Message': 'Method not allowed',
            'Status': 401
        })

class LogoutResource(Resource):
    @login_required
    def get(self):
        """ Delete user login from session """
        logout_user()
        return jsonify(
            {
                'Message': 'You are logged out',
                'Status': 200
            }
        )