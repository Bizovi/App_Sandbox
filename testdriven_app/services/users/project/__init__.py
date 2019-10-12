# services/users/project/__init__.py
import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__)

api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)


class User(db.Model):
    """
    The database model for users
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UsersPing(Resource):
    def get(self):
        return {
        'status': 'success',
        'message': 'here we go again ...'
    }


# import sys   # for debugging purposes
# print(app.config, file=sys.stderr)  # docker-compose logs

api.add_resource(UsersPing, '/users/ping')
