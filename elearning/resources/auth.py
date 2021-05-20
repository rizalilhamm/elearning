from flask import Response, request, jsonify, url_for, redirect
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
            return jsonify("User logged in")

        if request.method == "POST":
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            user_level = None
            user = User.query.filter_by(email=email).first()
            
            if user:
                return jsonify({"Message": "Email has been registered, try another one"})
            
            if password != confirm_password or len(password) != len(confirm_password):
                return jsonify({
                    "message": "Password is not same!",
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
                return "Email tidak diizinkan!"

            new_user = User(firstname=firstname, lastname=lastname, email=email, password=password, user_level=user_level)
            new_user.hash_password()
            
            db.session.add(new_user)
            db.session.commit()

            return jsonify(
                {
                    "Username": firstname
                }
            )

        # except Exception as e:
            # return jsonify({"message": "Masih ada yang salah"})

class LoginResource(Resource):
    def post(self):
        if current_user.is_authenticated:
            return jsonify("User logged in")

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            
            if not user or not user.check_password(password):
                return jsonify({
                    "Message": "invalid email or password!",
                })
            
            login_user(user)
            return jsonify({
                    "Username": user.firstname + ' ' + user.lastname
            })

class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return jsonify(
            {
                "message": "You are logged out"
            }
        )