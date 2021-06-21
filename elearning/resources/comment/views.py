from flask import request, jsonify
from flask_restful import Resource
from flask_login import login_required, current_user

from elearning import db
from elearning.models import Comment

class ClassCommentResource(Resource):
    @login_required
    def post(self, class_id):
        if request.method == 'POST':
            if 'class_comment' not in request.form:
                return jsonify({
                    'Message': 'You do not comment anything in this class',
                    'Status': 200
                })
            class_comment = request.form['class_comment']
            new_comment = Comment(comment_text=class_comment, user_id=current_user.id, class_id=class_id)
            db.session.add(new_comment)
            db.session.commit()
        
            return jsonify({
                'Message': 'Success',
                'Comment': str(new_comment),
                'Status': 200
            })

    @login_required
    def get(self, class_id):
        comments = [c for c in Comment.query.filter_by(class_id=class_id).all() if not c.task_id]
        return jsonify({
            'Message': 'Success',
            'Comment': str(comments),
            'Status': 200
        })


class TaskCommentResource(Resource):
    @login_required
    def post(self, class_id, task_id):
        if request.method == 'POST':
            if 'task_comment' not in request.form:
                return jsonify({
                    'Message': 'You do not comment anything in this Task',
                    'Status': 200
                })
            
            task_comment = request.form['task_comment']
            new_comment = Comment(comment_text=task_comment, user_id=current_user.id , class_id=class_id, task_id=task_id)
            db.session.add(new_comment)
            db.session.commit()
            
            return jsonify({
                'Message': 'Success',
                'Comment': str(new_comment),
                'Status': 200
            })


    @login_required
    def get(self, class_id, task_id):
        comments = Comment.query.filter_by(task_id=task_id).all()
        return jsonify({
            'Message': 'Success',
            'Comment': str(comments),
            'Status': 200
        })
    