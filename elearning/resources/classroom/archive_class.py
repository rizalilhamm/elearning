from flask import jsonify
from flask_login import current_user
from flask_restful import Resource

from elearning import elearning, db
from elearning.models import User, Class


class ArchivedsClassroom(Resource):
    def get(self):
        archived_class = set()
        for cls in Class.query.join(User.classes).filter(User.email==current_user.email).all():
            if cls.archived == False:
                archived_class.add(cls)

        return jsonify({
            "class": str(archived_class)
            })

class ArchivedClassroom(Resource):
    def post(self, class_id):
        cls = Class.query.get(class_id)
        if cls.archived == False:
            cls.archived = True
        else:
            cls.archived = False
        db.session.commit()
        
        return jsonify({
            "Message": "Archived!",
            'Status': 200
        })