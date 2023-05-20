from enum import Enum
from flask import request
from flask_restful import abort, Resource, reqparse, fields, marshal_with
from flask_login import login_required, login_user, current_user, logout_user
from backend import Table, FormattedTable, AggregatableTable, create_hash_password

class Membership(Enum):
    free = 0
    basic = 1
    premium = 2


users_profile_fields = {
    "first_name": fields.String,
    "last_name": fields.String,
    "username": fields.String,
    "email_address": fields.String,
    "membership": fields.Integer
}


class User:
    def __init__(self, user):
        self.username = user.username
        self.email_address = user.email_address
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.password = user.password
        self.membership = Membership(user.membership)
        
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.username

class UserProfile(Resource):
    @login_required
    def get(self, username):
        if current_user.username == username:
            users_table = AggregatableTable.access_table("users")
            return users_table.query(username=username)[0]
        return {"message": "Not a valid URL!"}


class SignUp(Resource):
    def post(self):
        password = create_hash_password(request.form["password"])
        kwargs = request.form.to_dict()
        kwargs["password"] = password
        kwargs["membership"] = int(kwargs["membership"])
        users_table = AggregatableTable.access_table("users")
        users_table.insert(**kwargs)
        return {
            "message" : "request to add user was successsful."
        }


class Login(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        users_table = AggregatableTable.access_table("users")
        user = users_table.query(username=username)
        if not user:
            raise Exception(f"User with username: `{username}` does not exist.")
        user = User(user[0])
        if user.password == create_hash_password(password):
            resp = login_user(user, remember=True)
            if resp:
                return {"message": "Login Successful!"}
        return {"message": "Please check your Credentials!"}

class Logout(Resource):
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            return {"message":"Logout Successful!"}
        return {"message":"Please check the URL!"}


class MembershipFeatures(Resource):
    """
    This class lists all the features that are set out to be provided among all
    3 classes of membership type.
    """
    def get(self):
        return {
            "free_feats" : Table._features(),
            "basic_feats" : FormattedTable._features(),
            "premium_feats" : AggregatableTable._features(),
        }

