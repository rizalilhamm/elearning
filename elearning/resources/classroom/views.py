from flask import jsonify, request
from flask_restful import Resource
from flask_login import current_user, login_required

from elearning import db
from elearning.models import User, Class    
from elearning.resources.errors import SchemaValidationError

def validate_lecture(user_level):
    return user_level < 2
class ClassroomsResource(Resource):
    @login_required
    def post(self):
        """ Function used to create new class that only admin or lecture can use it
        return:
            tell user the class created! """
        if validate_lecture(current_user.user_level):
            if request.method == "POST":
                new_classname = request.form['new_classname']
                if Class.query.filter_by(classname=new_classname).first():
                    return jsonify({
                        "Message": "Class is available",
                        "Status": 400
                    })
                new_class = Class(classname=new_classname)
                new_class.users.append(current_user)
                db.session.add(new_class)
                db.session.commit()

                return jsonify({
                    "Message": "Class created", 
                    "Status": 201
                })
        else:
            return jsonify({
                "Message": "Only admin or lecture can Create a new Class",
                "Status": 403
            })

    @login_required
    def get(self):
        cu_classes = [str(cls) for cls in Class.query.join(User.classes).filter(User.email==current_user.email).all()]
        # cu_classes = str(Class.query.all())
        message = None

        if len(cu_classes) > 0:
            message = cu_classes
        else:
            message = "You have no Class yet"
        
        return jsonify({
            "Classes": message
        })
    

class ClassroomResource(Resource):
    @login_required
    def get(self, id):
        s_class = Class.query.join(User.classes).filter(User.email==current_user.email).filter_by(class_id=id).first()
        if s_class is None:
            return  jsonify({
                "Message": "Class not Found",
                "Status": 404
            })
        return jsonify({
            "Classname": str(s_class),
        })
    
    @login_required
    def put(self, id):
        if validate_lecture(current_user.user_level):
            s_class = Class.query.filter_by(class_id=id).first()
            if s_class is None:
                    return jsonify({
                        "Message": "class Not found",
                        "Status": 404
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

                new_student_email = request.form['new_student_email']
                student = User.query.filter_by(email=new_student_email).first()
                if not student:
                    return jsonify({
                        'Message': 'Student with {} not found'.format(new_student_email),
                        'Status': 400
                    })
                
                s_class.users.append(student)

                s_class.classname = new_classname
                db.session.commit()

                return jsonify({
                      "Message": 'Classname updated to {}'.format(str(s_class.classname))
                })
        else:
            return jsonify({
                "Message": "Only Admin or lecture can update the class",
                "Status": 403
            })