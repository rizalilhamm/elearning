from flask import request
from flask.json import jsonify
from flask_restful import Resource
from flask_login import current_user, login_required

from elearning import db
from elearning.models.databasemodels import Class, User

class ParticipantsResource(Resource):
    @login_required
    def get(self, class_id):
        """ Get all participant from a particular class """
        s_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        participants = []
        for user in s_class.users:
            us = {}
            us['User_id'] = user.id
            us['Name'] = user.firstname + ' ' + user.lastname
            us['User_level'] = user.user_level
            participants.append(us)
        return jsonify({
            'Participants': participants,
            'Status': 200
        })
    
    @login_required
    def post(self, class_id):
        """ Lecturer has ability to add new participant to a class by input student email """
        s_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        
        if request.method == 'POST':
            if 'user_email' not in request.form:
                return jsonify({
                    'Message': 'User email required!',
                    'Status': 400
                })

            user_email = request.form['user_email']
            check_user = User.query.filter_by(email=user_email).first()
            if not check_user:
                message = 'User whit {} not found'.format(user_email)
            elif check_user in s_class.users:
                message = 'User with that email already in this Class'

            else:
                s_class.users.append(check_user)
                db.session.commit()
                return jsonify({
                    'Message': 'Student with {} email added to this class'.format(check_user),
                    'Status': 200
                })
            
            return jsonify({
                'Message': message,
                'Status': 400
            })

class ParticipantResource(Resource):
    @login_required
    def get(self, class_id, index):
        """ Get a particular Student profile """
        s_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        
        if index > len(s_class.users):
            return jsonify({
                'Message': f'You only have {len(s_class.users)} participants in this class',
                'Status': 400
            })

        participant = s_class.users[index-1]
        return jsonify({
            'Name': str(participant),
            'User_id': participant.id,
            'Status': 200
        })
    @login_required
    def delete(self, class_id, index):
        pass