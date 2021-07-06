# import elearning
# from flask import flash, request, redirect, url_for, render_template
# from elearning import elearning
# from elearning.models import User

# user_email_domain = ['lecture.ar-raniry.ac.id', 'student.ar-raniry.ac.id']
# @elearning.route('/manual-register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         firstname = request.form['firstname']
#         lastname = request.form['lastname']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         user_level = None
        
#         if (firstname.replace(' ', '') or lastname.replace(' ', '') or email or password) == '':
#             flash('Semua field wajib diisi!')
#             return redirect(url_for('register'))
        
#         _, email_domain = email.split('@')
#         for i in range(len(user_email_domain)):
#             if email_domain == user_email_domain[i]:
#                 if i == 0:
#                     user_level = 1
#                 elif i == 1:
#                     user_level = 2
#                 break
        
#         if User.query.filter_by(email=email).first():
#             flash('Email sudah terdaftar coba yang lain')
#             return redirect(url_for('register'))

#         if user_level == None:
#             flash('Email tidak diizinkan')
#             return redirect(url_for('register'))
            
#         if (password != confirm_password) or (len(password) != len(confirm_password)):
#             flash('Password harus sama')
#             return redirect(url_for('register'))
        
#         new_user = User(firstname=firstname, lastname=lastname, email=email, user_level=user_level)
#         new_user.hash_password()
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Register Berhasil, register another email!')
#         return redirect(url_for('register'))

#     return render_template('register.html')