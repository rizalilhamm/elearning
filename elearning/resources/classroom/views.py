from elearning.models.databasemodels import Theory
import os
from flask import jsonify, request
from flask_restful import Resource
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from elearning import db, elearning
from elearning.models import User, Class 
from elearning.resources.errors import SchemaValidationError

def validate_lecture(user_level):
    return user_level < 2

def validate_student(user_level):
    return user_level == 2
class ClassroomsResource(Resource):
    @login_required
    def post(self):
        """ Function used to create new class that only admin or lecture can use it
        return:
            tell user the class created! """
        if validate_lecture(current_user.user_level):
            if request.method == 'POST':
                new_classname = request.form['new_classname']
                if Class.query.filter_by(classname=new_classname).first():
                    return jsonify({
                        'Message': 'Class is available',
                        'Status': 400
                    })
                new_class = Class(classname=new_classname)
                new_class.users.append(current_user)
                db.session.add(new_class)
                db.session.commit()

                return jsonify({
                    'Message': 'Class created', 
                    'Status': 201
                })
        else:
            return jsonify({
                'Message': 'Only admin or lecture can Create a new Class',
                'Status': 403
            })

    @login_required
    def get(self):
        cu_classes = [str(cls) for cls in Class.query.join(User.classes).filter(User.email==current_user.email).all()]
        message = None

        if len(cu_classes) > 0:
            message = cu_classes
        else:
            message = 'You have no Class yet'
        
        return jsonify({
            'Classes': message
        })
class ClassroomResource(Resource):
    @login_required
    def get(self, class_id):
        current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()
        
        if current_class == None:
            return jsonify({
                'Message': 'Class not found!',
                'Status': 400
            })
        return jsonify({
            'Classname': str(current_class),
            'Status': 200
        })
    
    @login_required
    def put(self, class_id):
        if validate_lecture(current_user.user_level):
            # s_class = Class.query.filter_by(class_id=class_id).first()
            current_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=class_id).first()

            if current_class is None:
                    return jsonify({
                        'Message': 'Class Not found',
                        'Status': 404
                    })
            if request.method == 'PUT':
                if 'new_classname' not in request.form:
                    return jsonify({
                        'Message': 'Type new Classname',
                        'Status': 400
                    })
                new_classname = request.form['new_classname']
                if new_classname == '':
                    return jsonify({
                        'Message': 'Type new Classname',
                        'Status': 400
                    }) 

                current_class.classname = new_classname
                db.session.commit()

                return jsonify({
                      'Message': 'Classname updated to \'{}\''.format(str(current_class.classname))
                })
        else:
            return jsonify({
                'Message': 'Only Admin or lecture can update the class',
                'Status': 403
            })

def validate_class_theory(class_id):
    current_class = Class.query.get(class_id)
    path = elearning.config['UPLOAD_FOLDER'] + '/uploads/materials/{}/'.format(current_class.classname)
    if not os.path.isdir(path):
        os.makedirs(path)
    
    files = []
    for x in os.listdir(path):
        if x.endswith('.pdf'):
            files.append(x)
        
    return files

ALLOWED_EXTENTIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and \
        filename.split('.')[1].lower() in ALLOWED_EXTENTIONS
class TheoryResource(Resource):
    """
    Lecturer only
    1. Post: Lecture Upload materials to class
             File location in /elearning/uploads/theory/classes
             material name: "classname + theory title"
    2. Get all materials and show it in the class forum
    3. Delete a material
    """
    def post(self, class_id):
        current_class = Class.query.get(class_id)
        message = None
        if current_user.user_level <= 1:        
            if request.method == 'POST':
            
                if 'material' not in request.files or 'material_title' not in request.form:
                    message = 'No field to input!'
                
                else:
                    material = request.files['material']
                    material_title = request.form['material_title']

                    if allowed_file(material.filename):
                        if (material.filename == '') or (material_title == ''):
                            message = 'All fields are required!'
                        else:
                            if material_title == str(Theory.query.filter_by(theory_name=material_title).first()):
                                message = 'This title was used, try another one!'
                            else:
                                path = elearning.config['UPLOAD_FOLDER'] + '/uploads/materials/{}/'.format(current_class.classname)
                                file_extention = '.{}'.format(material.filename.split('.')[1].lower())
                                if not os.path.isdir(path):
                                    os.makedirs(path)
                                material_name = secure_filename('{}-{}'.format(current_class.classname, material_title + file_extention))
                                material.save(os.path.join(path, material_name))
                                new_theory = Theory(theory_name=material_title, class_id=current_class.class_id)
                                db.session.add(new_theory)
                                db.session.commit()
                                message = 'Material \'{}\' submitted!'.format(material_title)
                    else:
                        message = 'File not allowed'

                return jsonify({
                    'Message': message
                })
        else:
            return jsonify({
                'Message': 'Only admin or lecturer can post material'
            })