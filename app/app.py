import jwt
from functools import wraps
from datetime import datetime, timedelta
from flask import Flask, request
from flask_login import UserMixin
from flask_restful import Resource, Api
from models.user import Users as DB_USERS

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
        print(user)
        output_user = {"users_id": user.users_id,
                       "email": user.email,
                       "username": user.username}
        return output_user, 200

    def put(self, users_id):
        body = request.json
        user = DB_USERS.update_user(users_id, body)
        output_user = {"email": user.email,
                       "username": user.username}
        return output_user, 200

    def delete(self, users_id):
        DB_USERS.delete_user(users_id)
        return 204


class Users(Resource):
    def get(self):
        list_of_users = []
        users = DB_USERS.get_all_users()
        print(users)
        # users == [<User 86/as/as>, <User 87/ass/ass>]

        for user_data in users:
            users_info = {"users_id": user_data.users_id,
                          "email": user_data.email,
                          "username": user_data.username,
                          "password": user_data.password_hash
                          }
            list_of_users.append(users_info)
        return list_of_users, 200

    def post(self):
        body = request.json
        email = body.get("email")
        username = body.get("username")
        password = body.get("password")
        user = DB_USERS.registation_user(email, username, password)
        user = DB_USERS.get_user_by_email(email)
        output_user = {
            "users_id": user.users_id,
            "email": user.email,
            "username": user.username,
            "password": user.password_hash,
        }

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
                               "lol", algorithm='HS256').decode()
            print(token)
            print(type(token))
            # token = {"token_fied": user.token_field}
            # print(save_token)
            return token

        # auth = request.authorization
        # if not auth or not auth.username or not auth.password:
        #     return "Password or email is incorrect", 401
        #
        # user = DB_USERS.get_user_by_email(auth.username)
        # if not user:
        #     return "Could not verify", 401
        # if DB_USERS.check_password(user.password_hash, auth.password):
        #     # if user and DB_USERS.check_password(user.password_hash, password):
        #     token = jwt.encode({"users_id": DB_USERS.users_id, "exp": datetime.utcnow() + timedelta(hours=24)})
        #     return jsonify({"token": token.decode("UTF-8")})
        # return "Please check your email or password", 401

    # auth = request.authorization
    # email = body.get("email")
    # password = body.get("password")
    # if not auth or not auth.username


class LogOut(Resource):
    def put(self):

        return DB_USERS.logout()



api.add_resource(Users, '/users')
api.add_resource(User, '/users/<users_id>')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
