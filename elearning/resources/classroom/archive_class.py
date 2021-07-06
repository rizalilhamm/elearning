from flask import jsonify, request
from flask_login import current_user, login_required
from flask_restful import Resource

from elearning import db
from elearning.models import User, Class


class ArchivedsClassroom(Resource):
    @login_required
    def get(self):
        """Get all class that archived by lecturer"""
        archived_classes = []
        for cls in Class.query.join(User.classes).filter(User.email==current_user.email).all():
            if cls.archived == True:
                archived_class = {}
                archived_class['Classname'] = cls.classname
                archived_class['Class_id'] = cls.class_id
                archived_class['Archived'] = cls.archived
                archived_classes.append(archived_class)
        
        message = "You have some archived class!"
        if len(archived_classes) <= 0:
            message = "You have no archived class!"
        
        return jsonify({
            "Message": message,
            "Archived_class": archived_classes,
            "Status": 200
            })

class ArchivedClassroom(Resource):
    @login_required
    def get(self, class_id):
        """Get a particular archived class"""
        current_class = Class.query.get(class_id)
        message = "This class is not archived!"
        
        if current_class.archived == True:
            message = "This class is archived!"
        
        return jsonify({
            "Message": message,
            "Classname": current_class.classname,
            "Archived": current_class.archived
            })

    @login_required
    def post(self, class_id):
        """The function used to archive a particular class that filtered by class ID
            only available for lecturer"""
        current_class = Class.query.get(class_id)
        message = None

        user_permission = current_user.user_level <= 1
        if user_permission:
            if request.method == 'POST':
                if current_class.archived == False:
                    current_class.archived = True
                    message = "Archived!"
                    db.session.commit()
                elif current_class.archived == True:
                    current_class.archived = False
                    message = "Unarchived!"
                    db.session.commit()

                return jsonify({
                    "Message": message,
                    "Class": current_class.classname,
                    "Archived": current_class.archived,
                    "Status": 200
                })
        else:
            message = "Only admin or lecturer can archive a class!"
            return jsonify({
                "Message": message,
                "Status": 400
            })