import os
import sys
from flask import Flask
from flask_restful import Api

from app_config import Config

# append path to system list
app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)

from app.routes.user_routes import HelloWorld, Users, User

api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<users_id>')
# from app.routes import tasks_routes
