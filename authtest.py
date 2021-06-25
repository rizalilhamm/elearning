import os
import unittest

from flask import app

from elearning import elearning, db
from elearning.models import User

basedir = os.path.abspath(os.path.dirname(__file__))

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.db_url = 'sqlite:///' + os.path.join(basedir, 'test.db')
        elearning.config['TESTING'] = True
        elearning.config['SQLALCHEMY_DATABASE_URI'] = self.db_url
        self.elearning = elearning.test_client()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_models(self):
        # create new lecture
        lecturer_1 = User(firstname='Rizal', lastname='Ilham', email='rizal@lecture.ar-raniry.ac.id')
        db.session.add(lecturer_1)
        db.session.commit()

        # create new student
        student_1 = User(firstname='Rizal', lastname='Ilham', email='rizal@student.ar-raniry.ac.id')
        db.session.add(student_1)
        db.session.commit()

        # create second student
        student_2 = User(firstname='Mardha', lastname='Tika', email='mardhatika@student.ar-raniry.ac.id')
        db.session.add(student_2)
        db.session.commit()
        print(User.query.all())
        # check all user are added to db
        assert len(User.query.all()) is 3