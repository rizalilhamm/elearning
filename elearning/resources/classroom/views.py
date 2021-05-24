import json
from flask import jsonify, request
from flask_restful import Resource
from flask_login import current_user, login_required

from elearning import db
from elearning.models import User, Class

class Classroom(Resource):
    @login_required
    def get(self):
        cu_classes = str(Class.query.join(User.classes).filter(User.email==current_user.email).all())

        return jsonify({
            "Classes": cu_classes,
        })


class classroomSelect(Resource):
    @login_required
    def get(self, id):
        s_class = Class.query.filter_by(class_id=id).first()
        if s_class is None:
            return  jsonify({
                "Message": "Index out of range",
            })
        return jsonify({
            "Classname": s_class.classname,
        })
    
    @login_required
    def put(self, id):
        if current_user.user_level == 2:
            return jsonify({
                "Message": "Access denied!",
            })
        new_classname = request.form['new_classname']
        s_class = Class.query.filter_by(class_id=id).first()

        if s_class is None:
            return jsonify({
                "Message": "Not found",
            })
        
        s_class.classname = new_classname
        db.session.commit()

        return jsonify({
            "Message": s_class.classname
        })