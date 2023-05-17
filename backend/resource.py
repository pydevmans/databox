from enum import Enum
from flask import request
from flask_restful import abort, Resource, reqparse, fields, marshal_with
from flask_login import login_required
from backend import Table, FormattedTable, AggregatableTable, create_hash_password

class MembershipTypes(Enum):
    free = 0
    basic = 1
    premium = 2

users = AggregatableTable.access_table("users")

users_fields = {
    "first_name": fields.String,
    "last_name": fields.String,
    "username": fields.String,
    "email_address": fields.String,
    "membership": fields.Integer
}


class User(Resource):
    
    def __init__(self):
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = None
    
    def get_id(self):
        users.aggregate.equal("username", username)
        return users.username

    @login_required
    @marshal_with(users_fields)
    def get(self, username):
        return {"message": "Login Success"}

class UserCreation(Resource):
    def post(self):
        password = create_hash_password(request.form["password"])
        kwargs = request.form.to_dict()
        kwargs["password"] = password
        users.insert(**kwargs)
        return {
            "message" : "request to add user was successsful."
        }

class Login(Resource):
    def post(self):
        pass

class Logout(Resource):
    def post(self):
        pass

class Membership:
    def __init__(self, type = "free"):
        pass

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

