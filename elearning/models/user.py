from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from elearning import db

# active_class = db.Table("active_class",
    # db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    # db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.id', primary_key=True))    
# )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200),unique=True, nullable=False)
    username = db.Column(db.String(200),unique=True, nullable=False)
    password = db.Column(db.String(200))
    user_level = db.Column(db.Integer, nullable=False)
    # active_class = db.relationship("Classroom", secondary=tags, lazy="subquery",
                    # backref=db.backref("users", lazy=True))

    def hash_password(self):
        self.password = generate_password_hash(self.password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username