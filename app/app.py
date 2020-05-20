import jwt
from functools import wraps
from flask import Flask, request
from flask_restful import Resource, Api
from models.user import UserSchema, Users as DB_USERS
from marshmallow import ValidationError
from secret_key.secret_word_config_parser import SecretFile

app = Flask(__name__)
api = Api(app)


def token_getter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return "Token is missing"

        try:
            jwt.decode(token, "lol")

        except:
            return "Token is invalid"

        return func(*args, **kwargs)

    return wrapper


class User(Resource):

    def get(self, users_id):
        user = DB_USERS.get_user_by_id(users_id)
        schema_user = UserSchema(only=("users_id", "email", "username"))
        output_user = schema_user.dump(user)
        print(output_user)
        return output_user, 200

    def put(self, users_id):
        body = request.json
        user = DB_USERS.update_user(users_id, body)
        schema = UserSchema(only=("email", "username"))
        output_user = schema.dump(user)
        return output_user, 200

    def delete(self, users_id):
        DB_USERS.delete_user(users_id)
        return 204


class Users(Resource):
    def get(self):
        users = DB_USERS.get_all_users()
        print(users)
        schema = UserSchema(only=("users_id", "email", "username"), many=True)
        print(schema)
        all_users = schema.dump(users)
        return all_users, 200

    def post(self):
        body = request.json
        user_input_schema = UserSchema(only=("email", "password", "username"))

        print(user_input_schema)
        try:
            input_user = user_input_schema.load(body)
        except ValidationError as e:
            error = str(e)
            return error
        user = DB_USERS.registation_user(**input_user)
        user = DB_USERS.get_user_by_email(input_user.get("email"))
        user_output_schema = UserSchema(only=("email", "password_hash", "username"))
        output_user = user_output_schema.dump(user)

        return output_user, 201

    def delete(self):
        DB_USERS.delete_all_users()
        return 204


class LogIn(Resource):

    def post(self):

        body = request.json
        email = body.get("email")
        password = body.get("password")
        user = DB_USERS.get_user_by_email(email)
        # if not user.email and not DB_USERS.check_password(password):
        #     return True
        if user is None:
            return "user does not exist", 401
        elif user.check_password(password):

            token = jwt.encode({"users_id": user.users_id},
                               SecretFile.secret_key_getter(), algorithm='HS256').decode("UTF-8")
            if token:
                saved_token = DB_USERS.update_user_by_email(email, token)
                return saved_token, 200
            return token


#
# class LogOut(Resource):
#
#     def get(self):
#         DB_USERS.logout()


api.add_resource(Users, '/users')
api.add_resource(User, '/users/<users_id>')
api.add_resource(LogIn, '/login')
# api.add_resource(LogOut, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
