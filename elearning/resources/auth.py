from flask import Response, request, jsonify, url_for, redirect
from flask_restful import Resource
from flask_login import current_user, login_required, login_user

from elearning.models import User
from elearning import db

user_email_domain = ['lecture.ar-raniry.ac.id', 'student.ar-raniry.ac.id', 'gmail.com']

class SignupApi(Resource):
    def post(self):

        """ User level:
            0. Lecture
            1. Student
            2. User Optional """
        
        if current_user.is_authenticated:
            return jsonify("User logged in")

        if request.method == "POST":
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            user_level = None
            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({"Message": "Email sudah terdaftar silahkan coba email lain"})
            
            _, email_domain = email.split('@') 
            
            for i in range(len(user_email_domain)):
                if email_domain == user_email_domain[i]:
                    if i == 0:
                        user_level = 0
                    elif i == 1:
                        user_level = 1
                    elif i == 2:
                        user_level = 2
                    break

            new_user = User(email=email, username=username, password=password, user_level=user_level)
            new_user.hash_password()
            
            db.session.add(new_user)
            db.session.commit()
            return jsonify(
                {
                    "Username": username
                }
            )

        # except Exception as e:
            # return jsonify({"message": "Masih ada yang salah"})

class LoginApi(Resource):
    def post(self):
        if current_user.is_authenticated:
            return jsonify("User logged in")

        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            
            if not user:
                return jsonify("Email not regitered yet!")
        
            login_user(user)
            return jsonify(
                {
                    "Username": username
                }
            )