import os
import os
import re

basedir = os.path.abspath(os.path.dirname(__file__))

uri = os.getenv("DATABASE_URL")  # this will return error if does not exported
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

class Config(object):
     SECRET_KEY = os.getenv('SECRET_KEY') or 'ini-rahasia'
     SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'app.db')
                              # mysql://username:password@server/db (use this to connect in with MySQL database)
     SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') or True