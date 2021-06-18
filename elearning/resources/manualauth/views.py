from flask import flash, render_template, request, redirect
from flask.helpers import url_for
from flask_login import login_user, current_user, logout_user

from elearning import elearning, db
from elearning.models import User

user_email_domain = ['lecture.ar-raniry.ac.id', 'student.ar-raniry.ac.id']

@elearning.route('/', methods=['POST', 'GET'])
@elearning.route('/home', methods=['POST', 'GET'])
def home():
    if not current_user.is_authenticated:
        flash("Home You have to login before access this page")
        return redirect(url_for('register'))
    
    return render_template('home.html')

@elearning.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You must logout before register again!')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_level = None
        
        if (not firstname) or (not lastname) or (not email) or (not password) or (not confirm_password):
            flash('All fields are required!')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Pasword must equal")
            return redirect(url_for('register'))
        
        check_user = User.query.filter_by(email=email).first()
        if check_user:
            flash('That email has registered to our system, try another email or you can login')
            return redirect(url_for('register'))
        
        _, email_domain = email.split('@') 
        for i in range(len(user_email_domain)):
            if email_domain == user_email_domain[i]:
                if i == 0:
                    user_level = 1
                elif i == 1:
                    user_level = 2
                break
        new_user = User(firstname=firstname, lastname=lastname, email=email, password=password, user_level=user_level)
        new_user.hash_password()
        
        db.session.add(new_user)
        db.session.commit()
        flash("Login successfully!, now you can login")
        return redirect(url_for('register'))
    return render_template('register.html')

@elearning.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You must logout before register again!')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        check_user = User.query.filter_by(email=email).first()
        if not check_user or not check_user.check_password(password):
            flash('Email or password salah')
            return redirect(request.url)
        flash('Login berhasil')
        login_user(check_user)
        return redirect(url_for('home'))

    return render_template('login.html') 

@elearning.route('/logout', methods=['POST', 'GET'])
def logout():
    if not current_user.is_authenticated:
        flash('You are already logout, now you can try to login')
        return redirect(url_for('login'))
    
    flash('Are you sure want to logout')
    if request.method == 'POST':
        logout_user()
        flash('Welcome to our Elearning, this so fun and it is FREE!')
        return redirect(url_for('register'))
    
    return render_template('logout.html')