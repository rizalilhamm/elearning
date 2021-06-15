from flask import request, jsonify
from flask_restful import Resource
from flask_login import current_user, login_required

from elearning import db
from elearning.models import User, Class, Tasks, Answers

class AnswersResource(Resource):
    def get(self, class_id, task_id):
        # return all student answers from a particular class jika dia adalah Lecturer
        if current_user.user_level > 1:
            return "Not found"
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        if not current_class:
            return jsonify({
                'Message': 'Not found',
                'Status': 400
                
            })
        current_task = Tasks.query.join(Class.tasks).filter(Class.class_id==current_class.class_id).filter_by(class_id=class_id).first()
        if current_task == None:
            return jsonify({
                'Message': 'Not found',
                'Status': 400
            })
        else:
            answers = [str(answer) for answer in current_task.answers]

        return jsonify({
            'All responses': answers,
        })
    
class AnswerResource(Resource):
    def get(self, class_id, task_id, index):
        # return a particular student answer
        if current_user.user_level > 1:
            return jsonify({
                'Message': 'Not found',
                'Status': 404
            })
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        current_task = Tasks.query.join(Class.tasks).filter(Class.class_id==current_class.class_id).filter_by(task_id=task_id).first()
        current_answer = None
        if len(current_task.answers) < index:
            return jsonify({
                'Message': 'Not found',
                'Status': 404

            })
        else:
            current_answer = current_task.answers[index-1]
            owner = User.query.get(current_answer.owner)
            return jsonify({
                'Answer title': str(current_answer),
                'Owner': str(owner),
                'Score': '{} / 100'.format(current_answer.scores),
            })

    def post(self, class_id, task_id, index):
        # Lecturer can rate student answer at a particular task
        if current_user.user_level > 1:
            return 'not found'
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        current_task = Tasks.query.join(Class.tasks).filter(Class.class_id==current_class.class_id).filter_by(task_id=task_id).first()
        current_answer = current_task.answers[index-1]
        owner = current_answer.owner
        if request.method == 'POST':
            if not 'score'in request.form:
                return 'not not initialized'
            score = request.form['score']
            if score is None:
                return 'not not initialized'
            current_answer.scores = score
            db.session.commit()
        return jsonify({
            'Answer title': str(current_answer),
            'Owner': str(owner),
            'Score': '{} / 100'.format(current_answer.scores),

        })
    
    def put(self, class_id, task_id, index):
        # Lecturer has ability to update score after submited
        if current_user.user_level > 1:
            return 'Access denied'
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        current_task = Tasks.query.join(Class.tasks).filter(Class.class_id==current_class.class_id).filter_by(task_id=task_id).first()
        current_answer = current_task.answers[index-1]
        owner = current_answer.owner
        if request.method == 'PUT':
            if not 'score' in request.form:
                return 'not not initialized'
            score = request.form['score']
            if score is None or score > '100':
                return jsonify({
                    'Message': 'Something wrong',
                    'Status': 400
                })
            current_answer.scores = score
            db.session.commit()
        return jsonify({
            'Answer title': str(current_answer),
            'Owner': str(owner),
            'Score': '{} / 100'.format(current_answer.scores),
        })
    
    