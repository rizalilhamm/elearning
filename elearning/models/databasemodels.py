from werkzeug.security import generate_password_hash, check_password_hash
from elearning import db
from flask_login import UserMixin

user_identifier = db.Table(
    'user_identifier',
    db.Column('class_id', db.Integer, db.ForeignKey('classes.class_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(200))
    user_level = db.Column(db.Integer, nullable=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password, method='sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.firstname

class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(128),unique=True)
    users = db.relationship("User", secondary=user_identifier)

    def __repr__(self):
        return self.classname