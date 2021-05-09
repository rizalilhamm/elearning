import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
     SECRET_KEY = os.getenv('SECRET_KEY') or 'ini-rahasia'
     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
     SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') or True