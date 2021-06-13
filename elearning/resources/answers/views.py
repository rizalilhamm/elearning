from flask import request, jsonify
from flask_restful import Resource
from flask_login import current_user, login_required

from elearning import db
from elearning.models import User, Class, Tasks, Answers

# endpoint
# 127.0.0.1:5000/classes/<int:class_id>/tasks/<int:task_id>/result
# 127.0.0.1:5000/classes/<int:class_id>/tasks/<int:task_id>/answers/<int:answer_id>


# temukan semua tugas, 
class AnswersResource(Resource):
    def get(self, class_id, task_id):
        if current_user.user_level > 1:
            return "Not found"
        # mengembalikan semua hasil jawaban pada tugas tertentu
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        if not current_class:
            return "Class not found"
        current_task = Tasks.query.filter_by(class_id=current_class.class_id).first()

        answers = [str(answer) for answer in current_task.answers]

        return jsonify({
            'Semua jawaban': answers,
        })
    
class AnswerResource(Resource):
    def get(self, class_id, task_id, index):
        if current_user.user_level > 1:
            return 'Access denied'
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        current_task = Tasks.query.join(Class.tasks).filter(Class.class_id==current_class.class_id).filter_by(task_id=task_id).first()
        current_answer = None
        if len(current_task.answers) < index:
            return 'Index out of range'
        else:
            current_answer = current_task.answers[index-1]
            owner = User.query.get(current_answer.owner)
            return jsonify({
                'Jawaban sekarang': str(current_answer),
                'Owner': str(owner),
                'Score': '{} / 100'.format(current_answer.scores),
            })

    def post(self, class_id, task_id, index):
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
            'Jawaban sekarang': str(current_answer),
            'Owner': str(owner),
            'Score': '{} / 100'.format(current_answer.scores),

        })
    
    def put(self, class_id, task_id, index):
        if current_user.user_level > 1:
            return 'Access denied'
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        current_task = Tasks.query.join(Class.tasks).filter(Class.class_id==current_class.class_id).filter_by(task_id=task_id).first()
        current_answer = current_task.answers[index-1]
        owner = current_answer.owner
        if request.method == 'PUT':
            if not 'score'in request.form:
                return 'not not initialized'
            score = request.form['score']
            if score is None:
                return 'not not initialized'
            current_answer.scores = score
            db.session.commit()
        return jsonify({
            'Jawaban sekarang': str(current_answer),
            'Owner': str(owner),
            'Score': '{} / 100'.format(current_answer.scores),
        })
    
    