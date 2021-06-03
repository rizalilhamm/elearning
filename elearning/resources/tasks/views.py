import os
from werkzeug.utils import secure_filename
from flask import request
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
        """ Function used to push new task to a particular Class only admin or lecturer can do that
            param:
                class_id(int) -> the ID of a particular class
            url:
                127.0.0.1:5000/classes/<int:class_id>/tasks
            return:
                Task will be added to a Particular class if user is Admin or Lecturer """
        if validate_lecture(current_user.user_level):
            if request.method == 'POST':
                if 'task_title' not in request.form:
                    return jsonify({
                        'Message': 'Task title required',
                        'Status': 400
                    })

                task_title = request.form['task_title']
                if task_title == str(Tasks.query.filter_by(task_title=task_title).first()):
                    return jsonify({
                        'Message': 'Task with that title was created!',
                        'Status': 400 
                    })

                new_task = Tasks(task_title=task_title, class_id=class_id)
                
                if 'task_desc' in request.form:
                    new_task.task_desc = request.form['task_desc']
                db.session.add(new_task)
                db.session.commit()

                return jsonify({
                    'Message': 'Task added {}'.format(Class.query.get(class_id)),
                    'Tasks': str(new_task),
                    'Status': 200
                })
        else:
            return jsonify({
                'Message': 'Only admin or Lecture can Create new Task',
                'Status': 403
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
                'Message': 'Woohoo, no work due in soon!',
                'Status': 204
            })
        return jsonify({    
            'Tasks': tasks,
            'Message': 'You have some Tasks',
            'Status': 302
        })


ALLOWED_EXTENTIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[1].lower() in ALLOWED_EXTENTIONS

class TaskResource(Resource):
    def post(self, class_id, index):
        # The method for Student to Post their task
        if validate_student(current_user.user_level):
            if 'file' not in request.files:
                return jsonify({
                    'Message': 'All field are required',
                    'Status': 400
                })

            file = request.files['file']
            if file.filename == '':
                return jsonify({
                    'Message': 'No file selected',
                    'Status': 400
                })

            if file and allowed_file(file.filename):
                target = elearning.config['UPLOAD_FOLDER'] + '/uploads/{}'.format(current_user.lastname)
                s_class = Class.query.get(class_id)
                s_task = s_class.tasks[index-1]
                file_extention = '.{}'.format(file.filename.split('.')[1].lower())

                if not os.path.isdir(target):
                    os.makedirs(target)

                filename = secure_filename('{}-{}'.format(s_class.classname, str(current_user.firstname)) + file_extention)
                file.save(os.path.join(target, filename))
                return jsonify({
                    'Message': 'Uploaded!'
                })

            return jsonify({
                'Message': 'File not allowed!',
            })
        else:
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

            if request.method == "PUT":
                new_title = request.form['new_title']
                tasks[index-1].task_title = new_title
                if 'new_desc' in request.form:
                    tasks[index-1].task_desc = request.form['task_desc']
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
                'Message': 'you have only {} tasks in {} Class'.format(len(tasks), Class.query.get(class_id)),
                'Status': 404
            })
        task = tasks[index-1]
        return jsonify({
            'Task': str(task),
            'Task Description': str(task.task_desc)
        })
        
    def delete(self, task_id):
        pass
        