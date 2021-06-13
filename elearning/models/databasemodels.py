from sqlalchemy.orm import backref
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
        return '{} {}'.format(self.firstname, self.lastname)


class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(128),unique=True)
    theories = db.relationship('Theory', backref='classes', lazy=True)
    tasks = db.relationship("Tasks", backref='classes', lazy=True)
    users = db.relationship("User", secondary=user_identifier, backref=db.backref('classes', lazy='dynamic'))

    def __repr__(self):
        return self.classname

class Theory(db.Model):
    theory_id = db.Column(db.Integer, primary_key=True)
    theory_name = db.Column(db.String(200), unique=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)

    def __repr__(self):
        return self.theory_name

class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(200), unique=True)
    task_desc = db.Column(db.Text)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    answers = db.relationship('Answers', backref='tasks', lazy=True)
    
    def __repr__(self):
        return self.task_title

class Answers(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    answer_title = db.Column(db.String(200), nullable=False)
    scores = db.Column(db.String(30), default='Not checked yet')
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)

    def __repr__(self):
        return self.answer_title