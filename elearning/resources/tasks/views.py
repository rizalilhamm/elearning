from werkzeug.utils import secure_filename
from flask import request, redirect
from flask_login import current_user, login_required
from flask.json import jsonify
from flask_restful import Resource

from elearning import elearning, db
from elearning.resources.errors import SchemaValidationError, ExtentionError
from elearning.models import Class, Tasks
from elearning.resources.classroom.views import validate_lecture

def validate_student(user_level):
    return user_level == 2

class TasksResource(Resource):
    @login_required
    def post(self, class_id):
        """ Function used to push new task to a particular Class only admin or lecturer can use it
            param:
                class_id(int) -> the ID of a particular class
            url:
                127.0.0.1:5000/classes/<int:class_id>/tasks
            return:
                Task will be added to a Particular class if user is Admin or Lecturer """
        if validate_lecture(current_user.user_level):

            if request.method == 'POST':
                task_title = request.form["task_title"]

                if task_title == str(Tasks.query.filter_by(task_title=task_title).first()):
                    return jsonify({
                        "Message": "Task with that title was created!",
                        "Status": 400 
                    })

                new_task = Tasks(task_title=task_title, class_id=class_id)
                db.session.add(new_task)
                db.session.commit()

                return jsonify({
                    "Meesage": "Task added to" + Class.query.get(class_id),
                    "Tasks": new_task,
                    "Status": 200
                })
        else:
            return jsonify({
                "Message": "Only admin or Lecture can Create new Task",
                "Status": 403
            })
    
    def get(self, class_id):
        """ Select a particular Class and return all tasks if available
             param:
                class_id(int) -> the ID of a particular class
            url:
                127.0.0.1:5000/classes/<int:class_id>/tasks
            return:
                All tasks will be shown if available """
        
        tasks = [str(i) for i in Tasks.query.filter_by(class_id=class_id).all()] 
        if len(tasks) < 1:
            return jsonify({
                "Message": "Woohoo, no work due in soon!",
                "Status": 204
            })
        return jsonify({    
            "Tasks": tasks,
            "Message": "You have some Tasks",
            "Status": 302
        })


class TaskResource(Resource):
    def post(self, class_id, index):
        # The method for Student to Post their task
        if validate_student(current_user.user_level):
            pass

    @login_required
    def put(self, class_id, index):
        """ Function used to update a pasticular task Class only admin or lecturer can do it
            param:
                class_id(int) -> the ID of a particular class
                index(int) -> the index of a pasticular task in the list
            url:
                127.0.0.1:5000/classes/<int:class_id>/tasks/<int:index>
            return:
                The tasks title will be updated if there is a change """
        if validate_lecture(current_user.user_level):
            tasks = Tasks.query.filter_by(class_id=class_id).all()
            new_title = request.form['new_title']

            if request.method == "PUT":
                tasks[index-1].task_title = new_title
                db.session.commit()

            return jsonify({
                "Message": "Updated!",
                "Result": str(tasks[index-1])
            })
    
    @login_required
    def get(self, class_id, index):
        """ Function get a pasticular tasks based on it index in the list
            param:
                class_id(int) -> the ID of a particular class
                index(int) -> the index of a particular tasks
            url:
                127.0.0.1:5000/classes/<int:class_id>/tasks/<int:index>
            return:
                Get a pasticular task """
        tasks = Tasks.query.filter_by(class_id=class_id).all()
        if index > len(tasks):
            return jsonify({
                "Message": "you have only {} tasks in {} Class".format(len(tasks), Class.query.get(class_id)),
                "Status": 404
            })
        task = tasks[index-1]
        return jsonify({
            "Message": str(task)
        })
        