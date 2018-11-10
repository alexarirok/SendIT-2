"""Contains all endpoints to manipulate user information
"""
import datetime

from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse, inputs
from werkzeug.security import check_password_hash
import jwt

from ..models import models
from instance import config
from ..utils.decorators import admin_required


class User_Register(Resource):
    "Contains a POST method to register a new user"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])

        super().__init__()

    def post(self):
        """Register a new user"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get('email'):
                return make_response(jsonify({
                    "message" : "user with that email already exists"}), 400)

        if kwargs.get('password') == kwargs.get('confirm'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.create_user(username=kwargs.get('username'),
                                                 email=kwargs.get('email'),
                                                 password=kwargs.get('password'),
                                                 usertype="user")
                return make_response(jsonify(result), 201)
            return make_response(jsonify({
                "message" : "password should be atleast 8 characters"}), 400)
        return make_response(jsonify({
            "message" : "password and cofirm password should be identical"}), 400)

class AdminU_Register(Resource):
    "Contains a POST method to register a new user"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
            
        super().__init__()

    def post(self):
        """Register a new adminU"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get('email'):
                return make_response(jsonify({
                    "message" : "user with that email already exists"}), 400)

        if kwargs.get('password') == kwargs.get('confirm'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.create_user(username=kwargs.get('username'),
                                                 email=kwargs.get('email'),
                                                 password=kwargs.get('password'),
                                                 usertype="adminU")
                return make_response(jsonify(result), 201)
            return make_response(jsonify({
                "message" : "password should be atleast 8 characters"}), 400)
        return make_response(jsonify({
            "message" : "password and cofirm password should be identical"}), 400)

class Login(Resource):
    "Contains a POST method to login a user"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """login a user"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get("email") and \
                check_password_hash(models.all_users.get(user_id)["password"],
                                    kwargs.get("password")):

                token = jwt.encode({
                    'id' : user_id,
                    'usertype' : models.all_users.get(user_id)['usertype'],
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(weeks=3)},
                                   config.Config.SECRET_KEY)

                return make_response(jsonify({
                    "message" : "successfully logged in",
                    "token" : token.decode('UTF-8')}), 200)
        return make_response(jsonify({"message" : "invalid email address or password"}), 400)

class UserList(Resource):
    "Contains a POST method to register a new user and a GET method to get all users"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'usertype',
            required=False,
            default="user",
            location=['form', 'json'])
            
        super().__init__()

    @admin_required
    def post(self):
        """Register a new user or adminU or admin"""
        kwargs = self.reqparse.parse_args()
        for user_id in models.all_users:
            if models.all_users.get(user_id)["email"] == kwargs.get('email'):
                return make_response(jsonify({
                    "message" : "user with that email already exists"}), 400)

        if kwargs.get('password') == kwargs.get('confirm'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.create_user(username=kwargs.get('username'),
                                                 email=kwargs.get('email'),
                                                 password=kwargs.get('password'),
                                                 usertype=kwargs.get('usertype'))
                return make_response(jsonify(result), 201)
            return make_response(jsonify({
                "message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({
            "message" : "password and confirm password should be identical"}), 400)

    @admin_required
    def get(self):
        """Get all users"""
        return make_response(jsonify(models.User.all_users()), 200)

class User(Resource):
    """Contains GET PUT and DELETE methods for interacting with a particular user"""


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'usertype',
            required=True,
            default="user",
            location=['form', 'json'])
            
        super().__init__()

    @admin_required
    def get(self, user_id):
        """Get a particular user"""
        try:
            user = models.all_users[user_id]
            user = models.User.get_user(user_id)
            return make_response(jsonify(user), 200)

        except KeyError:
            return make_response(jsonify({"message" : "user does not exist"}), 404)

    @admin_required
    def put(self, user_id):
        """Update a particular user"""
        kwargs = self.reqparse.parse_args()
        if kwargs.get('password') == kwargs.get('confirm'):
            if len(kwargs.get('password')) >= 8:
                result = models.User.update_user(user_id=user_id,
                                                 username=kwargs.get('username'),
                                                 email=kwargs.get('email'),
                                                 password=kwargs.get('password'),
                                                 usertype=kwargs.get('usertype'))
                if result != {"message" : "user does not exist"}:
                    return make_response(jsonify(result), 200)
                return make_response(jsonify(result), 404)
            return make_response(jsonify({
                "message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({
            "message" : "password and confirm password should be identical"}), 400)

    @admin_required
    def delete(self, user_id):
        """Delete a particular user"""
        result = models.User.delete_user(user_id)
        if result != {"message" : "user does not exist"}:
            return make_response(jsonify(result), 200)
        return make_response(jsonify(result), 404)

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(User_Register, '/auth/userregister', endpoint='userregister')
api.add_resource(AdminU_Register, '/auth/adminUregister', endpoint='adminUregister')
api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:user_id>/parcels', endpoint='user')
