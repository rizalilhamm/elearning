import os
from werkzeug.utils import secure_filename
from flask import request
from flask_login import current_user, login_required
from flask.json import jsonify
from flask_restful import Resource

from elearning import elearning, db
from elearning.resources.errors import SchemaValidationError, ExtentionError
from elearning.models import Class, Tasks

def validate_lecture(user_level):
    return user_level <= 1

def validate_student(user_level):
    return user_level == 2

ALLOWED_EXTENTIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[1].lower() in ALLOWED_EXTENTIONS

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


def validate_student_task(class_id, task):
    """ if student has submit his task this will return your answer file else it return None """
    current_class = Class.query.get(class_id)
    path = elearning.config['UPLOAD_FOLDER'] + '/uploads/{}'.format(current_class.classname).lower()
    if not os.path.isdir(path):
        os.mkdir(path)

    files = []
    for x in os.listdir(path):
        if x.endswith('.pdf'):
            files.append(x)
    
    your_answer = None
    for file in files:
        if file == secure_filename('{}-{}.pdf'.format(task, current_user.firstname)):
            your_answer = file
            break
            
    return your_answer

class TaskResource(Resource):
    def post(self, class_id, index):
        # The method for Student to Post their task
        if index > len(Tasks.query.filter_by(class_id=class_id).all()):
            return 'Index out of range'

        current_class = Class.query.get(class_id)
        current_task = Tasks.query.filter_by(task_title=str(current_class.tasks[index-1])).first()
        message = None

        if validate_student(current_user.user_level) and (validate_student_task(class_id, current_task) == None):

            if request.method == 'POST':
                if validate_student_task(class_id, current_task) != None:
                    message = 'You have submit your task'
                else:
                    if 'file' not in request.files:
                        message = 'All field are required'
                    else:
                        file = request.files['file']
                        if file.filename == '':
                            message = 'No file selected!'
                        else:
                            if file and allowed_file(file.filename):
                                target = elearning.config['UPLOAD_FOLDER'] + '/uploads/{}'.format(str(current_class.classname).lower())
                                file_extention = '.{}'.format(file.filename.split('.')[1].lower())

                                if not os.path.isdir(target):
                                    os.makedirs(target)

                                filename = secure_filename('{}-{}'.format(current_task.task_title, str(current_user.firstname)) + file_extention)
                                file.save(os.path.join(target, filename))

                                current_task.answered_by = current_user.id
                                db.session.commit()

                                message = 'Task Submited by {}'.format(current_user.firstname)
                            else:
                                message = 'File not allowed!'

        elif validate_lecture(current_user.user_level):
            message = 'Only Student can upload the task response'
            
        else:
            message = 'You have submit task responce'
        return jsonify({
            'Message': message,
            'Status': 400
        })

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

            if request.method == 'PUT':
                new_title = request.form['new_title']
                tasks[index-1].task_title = new_title
                if 'new_desc' in request.form:
                    tasks[index-1].task_desc = request.form['task_desc']
                db.session.commit()

            return jsonify({
                'Message': 'Updated!',
                'Result': str(tasks[index-1])
            })
        else:
            return jsonify({
                'Message': 'Only admin or lecturer can update the task',
                'Status': 400
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
        if tasks == None:
            return 'This class has no task'
        if index > len(tasks):
            return jsonify({
                'Message': 'you have only {} tasks in {} Class'.format(len(tasks), Class.query.get(class_id)),
                'Status': 404
            })
        task = tasks[index-1]
        
        
        message = None
        if validate_student(current_user.user_level):
            your_answer = validate_student_task(class_id, task)
            if your_answer != None:
                message = 'Submitted!'
                return jsonify({
                    'Message': message,
                    'Terkumpul': your_answer,
                    'Task': str(task),
                    'Task Description': str(task.task_desc)
                })
            else:
                message = 'you do not submit your task yet'
                return jsonify({
                    'Message': message,
                    'Task': str(task)
                })
        else:
            message = 'You can update the task'
            return jsonify({
                'Message': message,
                'Task': str(task) 
            })
        
    def delete(self, task_id):
        pass
        